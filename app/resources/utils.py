import boto3
from functools import wraps
from flask import g, request

from ..models import User, Job
from ..views.home import BadRequestError


def get_aws_instances(n_workers=1):
    # get aws instance: 64bit ubuntu
    s = boto3.Session(profile_name='dev')
    ec2 = s.resource('ec2', region_name='us-east-1')
    rc = ec2.create_instances(ImageId='ami-d15a75c7',
                              InstanceType='t2.nano',
                              MinCount=1,
                              MaxCount=n_workers)
    if not rc:
        raise BadRequestError('Cannot get AWS instance.')
    return rc


def authenticate(f):
    """
    If authenticated, user_id is stored in g
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_str = request.headers.get('Authorization')
        token = auth_str.split(' ')[1] if auth_str else ''
        if token:
            user_id = User.decode_token(token)
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
        if not g.user.is_owner(job.id):
            raise BadRequestError('Current user does not own this job.')
        g.job = job
        return f(*args, **kwargs)
    return wrapper
