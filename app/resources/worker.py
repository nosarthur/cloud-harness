import boto3
import datetime
from flask import g
from flask_restful import Resource, reqparse, marshal_with, fields

from ..models import Worker
from .. import db
from ..views.home import BadRequestError
from utils import authenticate, get_aws_instances


worker_fields = {
    'id': fields.Integer,
    'job_id': fields.Integer,
    'instance_id': fields.String,
}


class WorkerAPI(Resource):

    decorators = [authenticate]

    # /api/workers/new
    @marshal_with(worker_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, location='json')
        parser.add_argument('n_workers', type=int, required=True,
                            location='json')
        args = parser.parse_args(strict=True)

        # form validation
        price = args.get('price')
        n_workers = args['n_workers']
        if n_workers > 5 or n_workers < 1:
            raise BadRequestError('Only 1 to 5 workers are allowed.')

        rc = get_aws_instances(n_workers)
        for x in rc:
            w = Worker(rc[0].id, price)
            db.session.add(w)
        db.session.commit()
        return w, 201

    def put(self, worker_id):
        """
        Worker periodically report to this access point.
        """
        w = Worker.query.get(worker_id)
        if w is None or w.date_finished:
            raise BadRequestError('Worker does not exist.')

        parser = reqparse.RequestParser()
        parser.add_argument('job_id', type=int, location='json')
        args = parser.parse_args(strict=True)

        job_id = args.get('job_id')
        if job_id:
            w.job_id = job_id
        else:
            w.date_modified = datetime.datetime.utcnow()
        db.session.add(w)
        db.session.commit()
        return 'Worker updated.', 204

    def delete(self, worker_id):
        """
        """
        w = Worker.query.get(worker_id)
        if w is None or w.date_finished:
            raise BadRequestError('Worker does not exist.')
        if not g.user.is_owner(w.job_id):
            raise BadRequestError('Current user does not own job %d.'
                                  % w.job_id)
        s = boto3.Session(profile_name='dev')
        ec2 = s.resource('ec2', region_name='us-east-1')
        rc = ec2.instances.filter(InstanceIds=[]).terminate()
        if not rc:
            raise BadRequestError('Cannot terminate AWS instance.')
        w.date_finished = datetime.datetime.utcnow()
        db.session.commit()
        return 'Worker deleted.', 204


class WorkerListAPI(Resource):

    decorators = [authenticate]

    # /api/workers/
    @marshal_with(worker_fields)
    def get(self):
        workers = Worker.query.all()
        return workers
