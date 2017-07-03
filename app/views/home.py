from flask import render_template, Blueprint

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home/index.html')


@home.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
