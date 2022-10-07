from logging.config import dictConfig

import flask_restful
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
login_manager = LoginManager()
api = flask_restful.Api()
migrate = Migrate()

logging_configuration = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./things_organizer.log",
            "formatter": "default",
            "maxBytes": 1024,
            "backupCount": 5,
        },
    },
    "root": {"level": "INFO", "handlers": ["wsgi", "file"]},
}

dictConfig(logging_configuration)
