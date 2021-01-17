import os
import click
from flask import Flask
from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import g
from flask_cors import CORS

__version__ = (0, 0, 1, "dev")

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the db subfolder
        SQLALCHEMY_DATABASE_URI="sqlite:///db/db.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CORS_HEADERS='Content-Type'
    )

    import backend.routes

    # initialize Flask-SQLAlchemy and the initdb command
    db.init_app(app)
    migrate.init_app(app, db)
    from backend import models

    # apply the blueprints to the app
    from backend import routes

    app.register_blueprint(routes.bp)

    # make url_for('index')
    app.add_url_rule("/", endpoint="index")

    return app
