from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from Teamwork.auth import login_required
from Teamwork.db import get_db
from Teamwork.queries import queries as q
import sqlite3

bp = Blueprint('tasks', __name__, url_prefix='/task')


@login_required
@bp.route('/create/<int:projectID>', methods=('GET', 'POST'))
def create_task(projectID):
    db = get_db()

    task = request.form.get('task')

    cur = db.cursor()
    with db:

        try:
            cur.execute(q.add_task, (task, g.user['UserID'], projectID,))

            taskID = cur.lastrowid

            cur.execute(q.add_taskhistory, (taskID, 'A',
                                            g.user['UserID'], task, task,))

            cur.close()
            db.commit()
        except sqlite3.Error as e:
            if db:
                db.rollback()
            flash(e)

        finally:
            if cur:
                cur.close()

    return redirect(url_for('projects.view_project', projectID=projectID))


@login_required
@bp.route('/delete', methods=('GET', 'POST'))
def delete_task():
    taskID = request.form.get('taskIDinput')
    return f'TaskID: "{taskID}"'
    projectID = get_db().execute(
        'SELECT ProjectID FROM Tasks WHERE TaskID = ?', (taskID,)).fetchone()[0]

    # redirect(url_for('projects.view_project', projectID=projectID))
    pass


@login_required
@bp.route('/edit/<int:taskID>', methods=('GET', 'POST'))
def edit_task(taskID):
    pass


@login_required
@bp.route('/<int:taskID>', methods=('GET', 'POST'))
def view_task(taskID):
    pass


@bp.before_app_request
def load_logged_in_user():
    userID = session.get('UserID')

    if userID is None:
        g.user = None
    else:
        g.user = get_db().execute(q.get_user_userID, (userID,)).fetchone()
        g.teams = get_db().execute(q.get_users_teams_userID, (userID, )).fetchall()
        g.ownedprojects = get_db().execute(
            q.get_user_owned_projects, (userID, )).fetchall()
        g.projects_involved_in = get_db().execute(
            q.get_user_involved_projects, (userID,)).fetchall()
