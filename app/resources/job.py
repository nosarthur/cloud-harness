from functools import wraps
from flask import abort, g, request
from flask_restful import Resource, reqparse, fields, marshal_with

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
        job = Job.query.get(kwargs.get('job_id'))
        if job is None:
            abort(404)
        g.job = job
        return f(*args, **kwargs)
    return wrapper


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_str = request.headers.get('Authorization')
        token = auth_str.split(' ')[1] if auth_str else ''
        if token:
            g.user_id = User.decode_token(token)
            user = User.query.get(int(g.user_id))
            if user:
                return f(*args, **kwargs)
        abort(401)
    return wrapper


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
        db.commit()
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

        job = Job(g.user_id, args['priority'])
        db.session.add(job)
        db.session.commit()
        return job, 201
