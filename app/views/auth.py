from flask import Blueprint, flash, url_for, redirect, request, render_template, jsonify
from flask_login import login_user, logout_user, login_required

from ..models import User
from .forms import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    #if not request.is_secure:
    #    return redirect(url_for('.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.validate(form.email.data, form.password.data)
#            return jsonify({'token': user.encode_token()})
        except Exception as e:
            flash('Login failed.' + str(e))
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        flash('You have logged in')
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('home.index'))
