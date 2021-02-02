from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from Teamwork.auth import login_required
from Teamwork.db import get_db
from Teamwork.queries import queries as q

import logging


bp = Blueprint('projects', __name__, url_prefix='/projects')


@login_required
@bp.route('/createproject/<int:teamID>', methods=('GET', 'POST',))
def create_project(teamID):
    teamMembers = get_db().execute(q.get_team_members_teamID, (teamID,)).fetchall()

    if request.method == 'GET':
        return render_template('projects/manageproject.html', action='Add', teamMembers=teamMembers, projectMembers=None)
    elif request.method == 'POST':
        db = get_db()

        projectMembers = request.form.getlist('projectMembers')
        projectDescription = request.form.get('description')
        projectName = request.form.get('projectName')
        projectOwner = g.user['UserID']

        cur = db.cursor()

        cur.execute(q.add_project, (projectName, projectDescription, teamID,))

        db.commit()

        new_ProjectID = cur.lastrowid

        for user in projectMembers:
            cur.execute(q.add_projectUsers, (new_ProjectID, user,))

        cur.close()
        db.commit()
        return redirect(url_for('teams.team', teamID=teamID))
    pass


@login_required
@bp.route('/editproject/<int:projectID>', methods=('GET', 'POST',))
def edit_project(projectID):
    db = get_db()
    project = db.execute(q.get_project_projectID, (projectID, )).fetchone()
    teamID = project['TeamID']
    projectMembers = db.execute(
        q.get_projectMembers_projectID, (projectID,)).fetchall()
    teamMembers = db.execute(
        q.get_team_members_teamID, (teamID,)).fetchall()

    if request.method == 'GET':
        return render_template('projects/manageproject.html', action='Edit',
                               project=project, projectMembers=projectMembers, teamMembers=teamMembers)
    elif request.method == 'POST':

        projectMembers = request.form.getlist('projectMembers')
        projectDescription = request.form.get('description')
        projectName = request.form.get('projectName')

        db.execute(q.clear_projectUsers, (projectID, ))

        db.execute(q.update_project, (projectName,
                                      projectDescription, projectID,))

        for user in projectMembers:
            get_db().execute(q.add_projectUsers, (projectID, user,))

        db.commit()
        return redirect(url_for('projects.view_project', projectID=projectID))


@login_required
@bp.route('/deleteproject/<int:projectID>', methods=('GET', 'POST',))
def delete_project(projectID):
    db = get_db()

    project = db.execute(q.get_project_projectID, (projectID,)).fetchone()
    teamID = project['TeamID']

    if request.method == 'GET':
        return render_template('projects/deleteproject.html', project=project)
    elif request.method == 'POST':
        db.execute(q.delete_project, (projectID,))
        db.execute(q.clear_projectUsers, (projectID,))
        db.commit()

        return redirect(url_for('teams.team', teamID=teamID))


@login_required
@bp.route('/viewproject/<int:projectID>', methods=('GET', 'POST',))
def view_project(projectID):
    db = get_db()
    project = db.execute(q.get_project_projectID, (projectID,)).fetchone()
    projectMembers = db.execute(
        q.get_projectMemberDetails_projectID, (projectID,)).fetchall()

    return render_template('projects/project.html', project=project, projectMembers=projectMembers)


@bp.before_app_request
def load_logged_in_user():
    userID = session.get('UserID')

    if userID is None:
        g.user = None
    else:
        g.user = get_db().execute(q.get_user_userID, (userID,)).fetchone()
        g.teams = get_db().execute(q.get_users_teams_userID, (userID, )).fetchall()
