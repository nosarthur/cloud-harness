import boto3
import datetime
from flask_restful import Resource, reqparse, marshal_with, fields

from ..models import Worker
from .. import db
from ..views.home import BadRequestError
from utils import authenticate


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
        parser.add_argument('job_id', type=int, location='json')
        parser.add_argument('n_workers', type=int, required=True,
                            location='json')
        args = parser.parse_args(strict=True)

        # form validation
        price = args.get('price')
        job_id = args.get('job_id')
        n_workers = args['n_workers']
        if job_id:
            pass
        if n_workers > 5 or n_workers < 1:
            raise BadRequestError('Only 1 to 5 workers are allowed.')

        # get aws instance: 64bit ubuntu
        s = boto3.Session(profile_name='dev')
        ec2 = s.resource('ec2', region_name='us-east-1')
        rc = ec2.create_instances(ImageId='ami-d15a75c7',
                                  InstanceType='t2.nano',
                                  MinCount=1,
                                  MaxCount=n_workers)
        if not rc:
            raise BadRequestError('Cannot get AWS instance.')
        for x in rc:
            w = Worker(rc[0].id, price)
            db.session.add(w)
        db.session.commit()
        return w, 201

    def delete(self, worker_id):
        w = Worker.query.get(worker_id)
        if w is None or w.date_finished:
            raise BadRequestError('Worker does not exist.')

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
