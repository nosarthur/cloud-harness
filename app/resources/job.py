from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with

from ..models import Job
from .. import db
from utils import authenticate, get_job


job_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'priority': fields.Integer,
    'status': fields.String
}


class JobAPI(Resource):
    """
    Read, update and delete for single job.
    """
    decorators = [get_job, authenticate]

    @marshal_with(job_fields)
    def get(self, job_id):
        return g.job

    @marshal_with(job_fields)
    def put(self, job_id):
        """
        Update job priority
        """
        job = g.job
        parser = reqparse.RequestParser()
        parser.add_argument('priority', type=int, required=True,
                            location='json')
        args = parser.parse_args(strict=True)

        job.priority = args['priority']
        db.session.commit()
        return job, 204

    # /api/jobs/start/<int:job_id>
    def post(self, job_id):
        """
        Start a chosen job
        """

        return 'success', 204

    # /api/jobs/stop/<int:job_id>
    def delete(self, job_id):
        # FIXME: do not delete from db, just stop it
        db.session.delete(g.job)
        db.session.commit()
        return 'Job stopped.', 204


class JobListAPI(Resource):
    """
    all jobs
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
