import os

from flask import Flask
from flask_migrate import Migrate

from things_organizer import utils
from things_organizer.extensions import database, login_manager, api
from things_organizer.login_utils import load_user
from things_organizer.web_app.about.resources import AboutResource
from things_organizer.web_app.auth.resources import (
    LoginResource, RegisterResource, LogoutResource
)
from things_organizer.web_app.categories.resources import (
    CategoryResource, EditCategoryResource,
    DeleteCategoryResource
)
from things_organizer.web_app.index.resources import HomeResource
from things_organizer.web_app.labels.resources import LabelResource
from things_organizer.web_app.reports.resources import ReportResource
from things_organizer.web_app.search.resources import SearchResource
from things_organizer.web_app.storages.resources import (
    StorageResource, EditStorageResource, DeleteStorageResource
)
from things_organizer.web_app.tags.resources import (
    TagResource, EditTagResource, DeleteTagResource
)
from things_organizer.web_app.things.resources import (
    AddThingResource, ThingResource, EditThingResource,
    DeleteThingResource
)


def create_app(debug: bool) -> Flask:
    """
    Function that creates a Flask application. App configuration is set here.

    Args:
        debug: debug mode enabled or not.

    Returns:
        app: a Flask app already configured to run.
    """
    app = Flask(__name__, static_url_path="/static")
    app.config.from_pyfile("config.py")

    if debug:
        app.config["DEBUG"] = True

    with app.app_context():
        create_dirs()
        configure_db(app)
        configure_migrations(app)
        configure_api(app)
        configure_login(app)

    return app


def create_dirs():
    """

    Returns:

    """
    dirs = [utils.DB_PATH, utils.LABEL_PATH, utils.REPORT_PATH]

    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


def configure_db(app: Flask):
    """Configure database ORM"""
    database.init_app(app)
    database.create_all()


def configure_migrations(app: Flask):
    """
    Configuration needed for DB migrations

    Args:
        app:

    """
    migrations_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'migrations'
    )
    print(migrations_dir)
    Migrate(app, database, compare_type=True, directory=migrations_dir)


def configure_login(app: Flask):
    """

    Args:
        app:

    Returns:

    """

    login_manager.session_protection = "strong"
    login_manager.login_view = "handle_login"
    login_manager.init_app(app)
    login_manager.user_loader(load_user)


def configure_api(app: Flask):
    """

    Args:
        app:

    Returns:

    """
    # Web Resources
    api.add_resource(
        RegisterResource, '/register',
        endpoint='handle_register'
    )
    api.add_resource(
        SearchResource, "/search",
        endpoint='handle_search'
    )
    api.add_resource(
        LoginResource, "/login",
        endpoint='handle_login'
    )
    api.add_resource(
        LogoutResource, "/logout",
        endpoint='handle_logout'
    )
    api.add_resource(
        AboutResource, "/about",
        endpoint='handle_about'
    )
    api.add_resource(
        HomeResource, '/', '/home',
        endpoint='handle_root'
    )
    api.add_resource(
        ThingResource, '/things',
        endpoint='handle_things'
    )
    api.add_resource(
        AddThingResource, '/add_thing',
        endpoint='handle_add_thing'
    )
    api.add_resource(
        EditThingResource, '/edit/thing/<int:int_id>',
        endpoint='handle_edit_thing'
    )
    api.add_resource(
        DeleteThingResource, '/delete/thing/<int:int_id>',
        endpoint='handle_delete_thing'
    )
    api.add_resource(
        CategoryResource, '/categories',
        endpoint='handle_categories'
    )
    api.add_resource(
        EditCategoryResource, '/edit/category/<int:int_id>',
        endpoint='handle_edit_category'
    )
    api.add_resource(
        DeleteCategoryResource, '/delete/category/<int:int_id>',
        endpoint='handle_delete_category'
    )
    api.add_resource(
        StorageResource, '/storages',
        endpoint='handle_storage'
    )
    api.add_resource(
        EditStorageResource, '/edit/storage/<int:int_id>',
        endpoint='handle_edit_storage'
    )
    api.add_resource(
        DeleteStorageResource, '/delete/storage/<int:int_id>',
        endpoint='handle_delete_storage'
    )
    api.add_resource(
        ReportResource, '/reports',
        endpoint='handle_report'
    )
    api.add_resource(
        TagResource, '/tags',
        endpoint='handle_tags'
    )
    api.add_resource(
        EditTagResource, '/edit/tag/<int:int_id>',
        endpoint='handle_edit_tag'
    )
    api.add_resource(
        DeleteTagResource, '/delete/tag/<int:int_id>',
        endpoint='handle_delete_tag'
    )
    api.add_resource(
        LabelResource, '/label/<int:int_id>',
        endpoint='handle_label'
    )
    # Initialize api
    api.init_app(app)
