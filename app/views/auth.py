from flask import (Blueprint, flash, url_for, redirect, session,
                   request, render_template, jsonify)
from flask_restful import reqparse

from ..models import User
from .forms import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST'])
def ajax_login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        location='json')
    parser.add_argument('password', type=str, required=True,
                        location='json')
    args = parser.parse_args(strict=True)
    try:
        user = User.validate(args['email'], args['password'])
    except ValueError as e:
        return jsonify({'token': ''}), 401
    return jsonify({'token': user.encode_token()})


@auth.route('/login', methods=['GET', 'POST'])
def login():
    #if not request.is_secure:
    #    return redirect(url_for('.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.validate(form.email.data, form.password.data)
        except Exception as e:
            flash('Login failed.' + str(e))
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        flash('You have logged in')
        session.permanent = True
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    flash('You have logged out.')
    return redirect(url_for('home.index'))
