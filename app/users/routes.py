from flask import render_template, Blueprint

users_bp = Blueprint('users', __name__, template_folder='templates')


@users_bp.route('/login')
def login():
    return render_template('login.html')
