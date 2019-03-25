"""

Simple and "lightweight" web application for fixing those common problems
of organizing that disaster or room/garage/lab
it is simple to use.

It also have an API that is enable for IOT purposes.

**Note:** we are using Semantic Version, for more information go to http://semver.org/
"""
import os

import flask
import flask_restful
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from things_organizer import utils
from things_organizer.api import categories, storages, tags, things


app = flask.Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////{}".format(os.path.join(utils.DB_PATH,
                                                                            "things_organizer.db"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16)

DB = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "handle_login"
login_manager.init_app(app)

API = flask_restful.Api(app)
API.add_resource(categories.CategoriesAPI, '/api/categories', '/api/categories/<int:int_id>')
API.add_resource(storages.StoragesAPI, '/api/storages', '/api/storages/<int:int_id>')
API.add_resource(tags.TagsAPI, '/api/tags', '/api/tags/<int:int_id>')
API.add_resource(things.ThingsAPI, '/api/things', '/api/things/<int:int_id>')

from things_organizer import views
from things_organizer.db import db_models

VERSION_INFO = {
    'MAJOR': 0,
    'MINOR': 1,
    'PATCH': 0,
}
__version__ = '{MAJOR:d}.{MINOR:d}.{PATCH:d}'.format(**VERSION_INFO)
__author__ = 'Juan Biondi'
__email__ = 'juanernestobiondi@gmail.com'
