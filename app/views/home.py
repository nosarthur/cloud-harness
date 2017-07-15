from flask import render_template, Blueprint, jsonify

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('index.html')


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


class BadRequestError(ValueError):
    pass


@home.app_errorhandler(BadRequestError)
def bad_request_handler(error):
    return bad_request(error.message)
