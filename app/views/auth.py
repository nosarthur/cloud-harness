from flask import Blueprint, jsonify
from flask_restful import reqparse

from ..models import User
from home import bad_request


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        location='json')
    parser.add_argument('password', type=str, required=True,
                        location='json')
    args = parser.parse_args(strict=True)
    try:
        user = User.validate(args['email'], args['password'])
    except ValueError as e:
        return bad_request('Wrong email password combination.')
    return jsonify({'token': user.encode_token()})


@auth.route('/logout')
def logout():
    return jsonify({'msg': 'You have logged out.'})
