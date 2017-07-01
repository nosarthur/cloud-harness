from flask import Flask, Blueprint, jsonify
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from config import config
from .views.auth import auth
from .views.home import home


bootstrap = Bootstrap()
login_manager = LoginManager()
db = SQLAlchemy()
#login_manager.login_view = 'auth.login'


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
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')

    bootstrap.init_app(app)
    login_manager.init_app(app)
    #db.init_app(app)

    # add resource
    api = Api(app)
    api.add_resource(Job, '/jobs/<string:job_id>')
#    api.add_resource(auth.AuthLogin, '/auth/login')
#    api.add_resource(auth.AuthRegister, '/auth/register')

    app.register_blueprint(home)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
