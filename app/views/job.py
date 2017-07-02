from flask import jsonify
from flask_restful import Resource, reqparse

from ..models import Job
from .. import db


class JobAPI(Resource):
    """
    Simple job
    """
    def get(self, job_id):
        return {'hello': 'world'}

    def post(self, job_id):
        parser = reqparse.RequestParser()

        return None

    def put(self, job_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args(strict=True)

        return None, 201

    def delete(self, job_id):
        return 'deleted', 204


class JobListAPI(Resource):
    """
    all jobs
    """
    def get(self):
        jobs = Job.query.all()
        return  jsonify([j.toJSON() for j in jobs])

    def post(self):
        parser = reqparse.RequestParser()
#        parser.add_argument('token', type=str, required=True, location='json')
        parser.add_argument('priority', type=int, location='json')
        parser.add_argument('token', type=str, required=True, location='json')
        args = parser.parse_args(strict=True)
        
        # figure out the user_id from token
        job = Job(1)
        db.session.add(job)
        db.session.commit()
        return None
