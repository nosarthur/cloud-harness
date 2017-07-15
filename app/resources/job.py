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
    decorators = [authenticate, get_job]

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

    def delete(self, job_id):
        job = g.job
        db.session.delete(job)
        db.session.commit()
        return 'Job deleted.', 204


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
        jobs = Job.query.all()
        return jobs

    @marshal_with(job_fields)
    def post(self):
        """
        Create a new job.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('priority', type=int, required=True,
                            location='json')
        args = parser.parse_args(strict=True)

        j = Job(g.user_id, args['priority'])
        db.session.add(j)
        db.session.commit()
        return j, 201
