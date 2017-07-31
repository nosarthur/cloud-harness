from functools import wraps
from flask import g, request

from ..models import User, Job
from ..views.home import BadRequestError


def authenticate(f):
    """
    If authenticated, user_id is stored in g
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_str = request.headers.get('Authorization')
        token = auth_str.split(' ')[1] if auth_str else ''
        if token:
            user_id = User.decodeToken(token)
            user = User.query.get(int(user_id))
            if user:
                g.user = user
                return f(*args, **kwargs)
        raise BadRequestError('Authentication failed.')
    return wrapper


def get_job(f):
    """
    If job exists in the database, stored it in g
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        job = Job.query.get(kwargs.get('job_id'))
        if job is None:
            raise BadRequestError('Job does not exist.')
        if not g.user.isOwner(job.id):
            raise BadRequestError('Current user does not own this job.')
        g.job = job
        return f(*args, **kwargs)
    return wrapper
