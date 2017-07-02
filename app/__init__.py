from flask import Flask, Blueprint, jsonify
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
login_manager = LoginManager()
db = SQLAlchemy()
#login_manager.login_view = 'auth.login'


from config import config
from .views.auth import auth
from .views.home import home
from .views.job import JobAPI, JobListAPI


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')

    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    # add resource
    api = Api(app)
    api.add_resource(JobAPI, '/jobs/<int:job_id>')
    api.add_resource(JobListAPI, '/jobs/')
#    api.add_resource(auth.AuthLogin, '/auth/login')
#    api.add_resource(auth.AuthRegister, '/auth/register')

    app.register_blueprint(home)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
