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
            g.user_id = User.decode_token(token)
            user = User.query.get(int(g.user_id))
            if user:
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
        g.job = job
        return f(*args, **kwargs)
    return wrapper
