from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from Teamwork.auth import login_required
from Teamwork.db import get_db
from Teamwork.queries import queries as q

bp = Blueprint('teams', __name__, url_prefix='/teams')


@login_required
@bp.route('/overview', methods=('GET', 'POST',))
def overview():
    if request.method == 'GET':

        if g.user is None:
            return redirect(url_for('auth.login'))

        teams = get_db().execute(q.get_users_teams_userID,
                                 (g.user['UserID'],)).fetchall()

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
                q.check_teams, (teamname, userID,)).fetchone()
        else:
            error = 'The team name cannot be only whitespaces'

        if teamcheck is not None:
            error = 'You are already the owner of a team by this name.'

        if error is None:
            cur = db.cursor()

            cur.execute(q.add_team, (teamname, userID, description,))

            db.commit()

            new_teamID = cur.lastrowid

            cur.execute(q.add_userTeam, (userID, new_teamID,))

            cur.close()
            db.commit()
            return redirect(url_for('teams.overview'))

        flash(error)

    return render_template('teams/createteam.html')


@bp.route('/findteam', methods=('GET', 'POST',))
def findteam():
    if request.method == 'GET':
        return render_template('teams/findteam.html')
    elif request.method == 'POST':
        search = request.form['search']
        error = None
        db = get_db()

        teams = db.execute(q.get_teams_search,
                           ('%' + search + '%', '%' + search + '%',)).fetchall()

        if teams == []:
            error = 'There were no teams with a name or owner similar to your search terms'
            flash(error)

        return render_template('teams/findteam.html', teams=teams, search_term=search)


@bp.route('/joinTeam/<int:teamID>', methods=('GET', 'POST',))
def jointeam(teamID):
    db = get_db()
    db.execute(q.add_userTeam, (g.user['UserID'], teamID,))
    db.commit()
    return redirect(url_for('teams.team', teamID=teamID))


@bp.route('<int:teamID>', methods=('GET', 'POST'))
def team(teamID):
    team = get_db().execute(q.get_team_info, (teamID,)).fetchone()
    teamMembers = get_db().execute(q.get_team_members_teamID, (teamID,)).fetchall()
    projects = get_db().execute(q.get_projects_teamID, (teamID,)).fetchall()
    user_on_team = get_db().execute(q.check_user_on_team,
                                    (g.user['UserID'], teamID,)).fetchone()[0]
    user_is_owner = get_db().execute('SELECT COUNT(*) FROM Teams WHERE TeamID = ? AND OwnerID = ?',
                                     (teamID, g.user['UserID'],)).fetchone()[0]

    return render_template('teams/team.html',
                           team=team,
                           teamMembers=teamMembers,
                           projects=projects,
                           user_on_team=user_on_team,
                           user_is_owner=user_is_owner)


@bp.before_app_request
def load_logged_in_user():
    userID = session.get('UserID')

    if userID is None:
        g.user = None
    else:
        g.user = get_db().execute(q.get_user_userID, (userID,)).fetchone()
        g.teams = get_db().execute(q.get_users_teams_userID, (userID, )).fetchall()
