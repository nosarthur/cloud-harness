from flask import render_template, Blueprint

auth = Blueprint('users', __name__, template_folder='templates')


@auth.route('/login')
def login():
    return render_template('login.html')
