from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate


db = SQLAlchemy()
moment = Moment()
migrate = Migrate()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        from . import forms
        from . import models
        from . import routes
        from . import utils
        # Initialize Global db
        db.create_all()

    migrate.init_app(app, db)
    moment.init_app(app)

    return app
