from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from werkzeug.exceptions import abort

from teamwork.auth import login_required
from teamwork.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')


@login_required
@bp.route('/overview', methods=('GET', 'POST',))
def overview():
    if request.method == 'GET':
        # if session.get('UserID') is None:
        if g.user is None:
            return redirect(url_for('auth.login'))
        return render_template('teams/overview.html')


@bp.before_app_request
def load_logged_in_user():
    userID = session.get('UserID')

    if userID is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Users WHERE UserID = ?', (userID,)
        ).fetchone()
