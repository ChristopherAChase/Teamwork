from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .auth import login_required
from .db import get_db
from .queries import queries as q
import sqlite3
import logging


bp = Blueprint('tasks', __name__, url_prefix='/task')


@bp.route('/create/<int:projectID>', methods=('GET', 'POST'))
@login_required
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


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete_task():
    db = get_db()
    taskID = request.form.get('taskIDinput')
    task = db.execute(q.get_task_info, (taskID, )).fetchone()
    projectID = task['ProjectID']

    db.execute(q.delete_task, (taskID,))
    db.commit()

    db.execute(q.add_taskhistory, (taskID, 'D',
                                   g.user['UserID'], task['Task'], task['Task']))
    db.commit()

    return redirect(url_for('projects.view_project', projectID=projectID))


@bp.route('/edit/', methods=('GET', 'POST'))
@login_required
def edit_task():
    db = get_db()
    taskID = request.form.get('taskIDinput')
    new_task_text = request.form.get('newTaskText')
    task = db.execute(q.get_task_info, (taskID, )).fetchone()
    projectID = task['ProjectID']

    db.execute(q.update_task, (new_task_text, taskID))
    db.commit()

    db.execute(q.add_taskhistory, (taskID, 'M',
                                   g.user['UserID'], task['Task'], new_task_text,))
    db.commit()

    return redirect(url_for('projects.view_project', projectID=projectID))


@bp.route('/<int:taskID>', methods=('GET', 'POST'))
@login_required
def view_task(taskID):
    db = get_db()
    current_user = g.user['UserID']

    if request.method == 'GET':
        task = db.execute(q.get_task_info, (taskID,)).fetchone()
        task_history = db.execute(q.get_task_history, (taskID,)).fetchall()
        comments = db.execute(q.get_task_comments, (taskID,)).fetchall()

        return render_template('tasks/task.html',
                               task=task,
                               task_history=task_history,
                               comments=comments,
                               current_user=current_user)
    if request.method == 'POST':
        comment = request.form.get('commentText')
        db.execute(q.add_task_comment, (comment, current_user, taskID,))
        db.commit()

        return redirect(url_for('tasks.view_task', taskID=taskID,))


@bp.route('/<int:taskID>', methods=('GET', 'POST'))
@login_required
def add_comment(taskID):
    db = get_db()
    comment = request.form.get('commentText')
    current_user = g.user['UserID']

    db.execute(q.add_task_comment, (comment, current_user, taskID,))
    db.commit()

    return redirect(url_for('tasks.view_task', taskID=taskID,))


@bp.route('complete/<int:taskID>', methods=('GET', 'POST'))
@login_required
def complete_task(taskID):
    db = get_db()

    task = db.execute(q.get_task_info, (taskID,)).fetchone()

    task_text = task['Task']
    taskEvent = 'U' if task['IsCompleted'] else 'C'

    cur = db.cursor()
    with db:

        try:
            cur.execute(q.toggle_task_completion_ID, (taskID,))

            cur.execute(q.add_taskhistory, (taskID, taskEvent,
                                            g.user['UserID'], task_text, task_text,))

            cur.close()
            db.commit()
        except sqlite3.Error as e:
            if db:
                db.rollback()
            logging.warn(e)

        finally:
            if cur:
                cur.close()

    return redirect(url_for('projects.view_project', projectID=task['ProjectID']))


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
