from flask import Flask
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()

from config import config
from .views.home import home
from .views.auth import auth
from .resources.job import JobAPI, JobListAPI


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    # app.config.from_pyfile('config.py')

    bootstrap.init_app(app)
    db.init_app(app)

    api = Api(app)
    api.add_resource(JobAPI, '/api/jobs/<int:job_id>')
    api.add_resource(JobListAPI, '/api/jobs/')

    app.register_blueprint(home)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
