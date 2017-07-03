from functools import wraps
from flask import flash, abort, g
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_login import login_required

from ..models import Job, User
from .. import db


job_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'priority': fields.Integer,
    'status': fields.String
}

def get_job(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        job = Job.query.get(job_id)
        if job is None:
            flash('Job does not exist.')
            abort(404)
        g.job = job
        return f(*args, **kwargs)
    return wrapper


class JobAPI(Resource):
    """
    Read, update and delete for single job.
    """
    decorators = [get_job]

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
        db.commit()
        return 'Job deleted.', 204


class JobListAPI(Resource):
    """
    all jobs
    """
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
        parser.add_argument('token', required=True, location='json')
        args = parser.parse_args(strict=True)

# FIXME: use authorization header instead of token
        user_id = User.decode_token(args['token'])
        if user_id == 0:
            return args, 401
        job = Job(user_id, args['priority'])
        db.session.add(job)
        db.session.commit()
        return job, 201
