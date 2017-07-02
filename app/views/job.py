from flask import jsonify
from flask_restful import Resource, reqparse

from ..models import Job
from .. import db


class JobAPI(Resource):
    """
    Simple job
    """
    def get(self, job_id):
        job = Job.query.filter_by(id=job_id).first()
        if job is None:
            # FIXME: abort 404?
            pass
        return jsonify(job.toJSON())

    def post(self, job_id):
        parser = reqparse.RequestParser()

        return None

    def put(self, job_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args(strict=True)


        #db.session.update(job)
        db.session.commit()

        return None, 201

    def delete(self, job_id):
        job = Job.query.filter_by(id=job_id).first()
        if job is None:
            pass
        db.session.delete(job)
        db.commit()
        return 'deleted', 204


class JobListAPI(Resource):
    """
    all jobs
    """
    def get(self):
        """
        Get all jobs
        """
        jobs = Job.query.all()
        return  jsonify([j.toJSON() for j in jobs])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('priority', type=int, location='json')
        parser.add_argument('token', type=str, required=True, location='json')
        args = parser.parse_args(strict=True)
        
        # FIXME: figure out the user_id from token
        job = Job(1)
        db.session.add(job)
        db.session.commit()
        return None
