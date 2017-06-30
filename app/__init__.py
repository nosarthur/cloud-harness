from flask import Flask, Blueprint, jsonify, render_template
from flask_login import LoginManager
from flask_restful import Resource, Api

from app.users.routes import users_bp

from config import config


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    login_manager.init_app(app)

    @app.route("/")
    def index():
        return render_template('index.html')

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # add resource

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(users_bp)

    return app
