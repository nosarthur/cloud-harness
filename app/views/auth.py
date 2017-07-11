from flask import Blueprint, flash, url_for, redirect, jsonify
from flask_restful import reqparse

from ..models import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def ajax_login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        location='json')
    parser.add_argument('password', type=str, required=True,
                        location='json')
    args = parser.parse_args(strict=True)
    try:
        user = User.validate(args['email'], args['password'])
    except ValueError as e:
        flash('Wrong email password combination.')
        return redirect(url_for('home.index'))
    return jsonify({'token': user.encode_token()})


@auth.route('/logout')
def logout():
    flash('You have logged out.')
    return redirect(url_for('home.index'))
