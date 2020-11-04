import flask_restful
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
login_manager = LoginManager()
api = flask_restful.Api()

