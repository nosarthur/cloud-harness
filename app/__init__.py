from flask import Flask, Blueprint, jsonify
from flask_login import LoginManager
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from app.users.routes import users_bp

from config import config


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


class Job(Resource):
    """
    Simple job
    """
    def get(self, job_id):
        return {'hello': 'world'}

    def put(self, job_id):
        return None, 201

    def delete(self, job_id):
        return 'deleted', 204


class JobList(Resource):
    """
    all jobs
    """
    def get(self):
        return 'all jobs'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    login_manager.init_app(app)
    db = SQLAlchemy(app)

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # add resource
    api.add_resource(Job, '/')
#    api.add_resource(auth.AuthLogin, '/auth/login')
#    api.add_resource(auth.AuthRegister, '/auth/register')

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(users_bp)

    return app
