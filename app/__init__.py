from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_restful import Resource, Api

from config import config


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    login_manager.init_app(app)

    @app.route("/")
    def hello():
        return "Hello World!"

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # add resource

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
