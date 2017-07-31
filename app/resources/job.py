from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with

from ..models import Job, Worker, get_aws_instances
from .. import db
from utils import authenticate, get_job
from ..views.home import BadRequestError


job_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'priority': fields.Integer,
    'status': fields.String
}


class JobStatusAPI(Resource):
    """
    Update job status as a worker.
    """
    decorators = [get_job, authenticate]

    @marshal_with(job_fields)
    def put(self, job_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True, location='json')
        parser.add_argument('result_url', type=str, location='json')
        args = parser.parse_args(strict=True)

        job_status = g.job.getStatus()
        job_status.goto(args.status)

        if args.result_url:
            g.job.result_url = args['result_url']
        db.session.add(g.job)
        db.session.commit()
        return g.job, 204


class JobAPI(Resource):
    """
    Start, update, and stop a single job as a user.
    """
    decorators = [get_job, authenticate]

    def get(self, job_id):
        """
        Start a waiting job
        """
        if g.job.status != 'WAITING':
            raise BadRequestError('Job is not waiting.')
        rc = get_aws_instances(1, on_demand=True)
        w = Worker(rc[0].id, g.job.id)
        db.session.add(w)
        db.session.commit()
        return 'success', 204

    @marshal_with(job_fields)
    def put(self, job_id):
        """
        Update job priority as a user.
        """
        job = g.job
        parser = reqparse.RequestParser()
        parser.add_argument('priority', type=int, required=True,
                            location='json')
        args = parser.parse_args(strict=True)

        job.priority = args['priority']
        db.session.commit()
        return job, 204

    def delete(self, job_id):
        """
        Stop a running job
        """
        w = Worker.query.filter_by(job_id=g.job.id).first()
        w.stop()
        g.job.stop()
        db.session.add_all([w, g.job])
        db.session.commit()
        return 'Job stopped.', 204


class JobListAPI(Resource):
    """
    API for getting all jobs and add one job.
    """
    decorators = [authenticate]

    @marshal_with(job_fields)
    def get(self):
        """
        Get all jobs
        """
        if g.user.is_admin:
            jobs = Job.query.all()
        else:
            jobs = g.user.jobs.all()
        return jobs

    @marshal_with(job_fields)
    def post(self):
        """
        Create a new job.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str, location='json')
        parser.add_argument('priority', type=int, required=True,
                            location='json')
        args = parser.parse_args(strict=True)

        j = Job(g.user.id, args['priority'])
        db.session.add(j)
        db.session.commit()
        return j, 201
