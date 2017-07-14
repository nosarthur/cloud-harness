from flask_restful import Resource, reqparse, marshal_with, fields

from ..models import Worker

worker_fields = {
    'id': fields.Integer,
    'job_id': fields.Integer,
    'ip': fields.String,
}

class WorkerAPI(Resource):

    @marshal_with(worker_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True,
                            location='json')
        parser.add_argument('num_worker', type=int, required=True,
                            location='json')
        args = parser.parse_args(strict=True)

        # get aws instance
        price = args['price']

        ip = '0.0.0.0'
        if 0:
            abort(406, description='Cannot get AWS instance.')
        w = Worker(ip, price)
        db.session.add(w)
        db.session.commit()
        return w, 201
