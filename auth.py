from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from Teamwork.db import get_db
from Teamwork.queries import queries as q

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['UserName']
        password = request.form['Password']
        email = request.form['Email']
        first_name = request.form['FirstName']
        last_name = request.form['LastName']

        db = get_db()
        error = None

        if not username:
            error = 'UserName is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not first_name:
            error = 'First name is required'
        elif not last_name:
            error = 'Last Name is required.'
        elif db.execute(q.get_user_userName, (username,)).fetchone() is not None:
            error = f'User {username} is already in use. Try a different one'
        elif db.execute(q.get_user_email, (email,)).fetchone() is not None:
            error = f'Email {email} is already in use. Do you maybe already'
            'have an account?'

        if error is None:
            db.execute(q.add_user, (username, generate_password_hash(
                password), email, first_name, last_name,))
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        username = request.form['UserName']
        password = request.form['Password']
        db = get_db()
        error = None

        user = db.execute(q.get_user_userName, (username,)).fetchone()

        if user is None:
            error = 'Incorrect user.'
        elif not check_password_hash(user['Password'], password):
            error = 'Invalid Password.'

        if error is None:
            session.clear()
            session['UserID'] = user['UserID']
            return redirect(url_for('teams.overview'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    userID = session.get('userID')

    if userID is None:
        g.user = None
    else:
        g.user = get_db().execute(q.get_user_userID, (userID,)).fetchone()
        g.teams = get_db().execute(q.get_users_teams_userID, (userID, )).fetchall()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
