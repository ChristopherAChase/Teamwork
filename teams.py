from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from werkzeug.exceptions import abort

from Teamwork.auth import login_required
from Teamwork.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')


@login_required
@bp.route('/overview', methods=('GET', 'POST',))
def overview():
    if request.method == 'GET':
        # if session.get('UserID') is None:
        if g.user is None:
            return redirect(url_for('auth.login'))

        get_teams = '''SELECT
                Teams.Name,
                Teams.Description,
                Users.Username
            FROM Teams
            INNER JOIN UserTeams ON Teams.TeamID = UserTeams.TeamID
            INNER JOIN Users ON Users.UserID = Teams.OwnerID
            WHERE UserTeams.UserID = ?'''

        teams = get_db().execute(get_teams, (g.user['UserID'],)).fetchall()

        if teams == []:
            return redirect(url_for('.noteams'))

        return render_template('teams/overview.html', teams=teams)


@login_required
@bp.route('/noteams', methods=('GET', 'POST',))
def noteams():
    return render_template('teams/noteams.html')


@login_required
@bp.route('/createteam', methods=('GET', 'POST',))
def createteam():
    if request.method == 'GET':
        return render_template('teams/createteam.html')
    elif request.method == 'POST':
        teamname = str(request.form['teamName']).strip()
        description = request.form['description']
        userID = g.user['UserID']

        db = get_db()
        error = None
        teamcheck = None

        if not teamname == '':
            teamcheck = db.execute(
                'SELECT * FROM Teams WHERE Name = ? AND OwnerID = ?', (
                    teamname, g.user['UserID'],)
            ).fetchone()
        else:
            error = 'The team name cannot be only whitespaces'

        if teamcheck is not None:
            error = 'You are already the owner of a team by this name.'

        if error is None:
            cur = db.cursor()

            cur.execute('INSERT INTO Teams (Name, OwnerID, Description) VALUES(?,?,?)',
                        (teamname, userID, description, ))

            db.commit()

            new_teamID = cur.lastrowid

            cur.execute(
                'INSERT INTO UserTeams (UserID, TeamID) VALUES(?,?)', (userID, new_teamID,))

            cur.close()
            db.commit()
            return redirect(url_for('teams.overview'))

        flash(error)

    return render_template('teams/createteam.html')


@bp.route('/findteam', methods=('GET', 'POST',))
def findteam():
    return render_template('teams/findteam.html')


@bp.before_app_request
def load_logged_in_user():
    userID = session.get('UserID')

    if userID is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Users WHERE UserID = ?', (userID,)
        ).fetchone()
