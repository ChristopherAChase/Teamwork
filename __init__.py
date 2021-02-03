from flask import Flask, render_template, redirect, url_for
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'teamwork.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db, auth, teams, project, tasks
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(project.bp)
    app.register_blueprint(tasks.bp)

    @app.route('/')
    def hello():
        return redirect(url_for('teams.overview'))

    return app
