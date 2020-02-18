from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from things_organizer.api import categories, storages, things, tags
from things_organizer.categories.routes import CategoryResource, EditCategoryResource
from things_organizer.common.routes import (
    HomeResource, LoginResource, RegisterResource, SearchResource,
    AboutResource, LabelResource, LogoutResource
)
from things_organizer.extensions import database, login_manager, api
from things_organizer.login_utils import load_user
from things_organizer.reports.routes import ReportResource
from things_organizer.storages.routes import StorageResource, EditStorageResource
from things_organizer.tags.routes import TagResource, EditTagResource
from things_organizer.things.routes import AddThingResource, ThingResource, EditThingResource


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

    configure_db(app)
    configure_migrations(app)
    configure_api(app)
    configure_login(app)

    return app


def configure_db(app: Flask):
    """Configure database ORM"""
    database.init_app(app)


def configure_migrations(app: Flask):
    """
    Configuration needed for DB migrations

    Args:
        app:

    """
    Migrate(app, database, compare_type=True)


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
    api.add_resource(RegisterResource, '/register', endpoint='handle_register')
    api.add_resource(SearchResource, "/search", endpoint='handle_search')
    api.add_resource(LoginResource, "/login", endpoint='handle_login')
    api.add_resource(LogoutResource, "/logout", endpoint='handle_logout')
    api.add_resource(AboutResource, "/about", endpoint='handle_about')
    api.add_resource(HomeResource, '/', '/home', endpoint='handle_root')
    api.add_resource(ThingResource, '/things', endpoint='handle_things')
    api.add_resource(AddThingResource, '/add_thing', endpoint='handle_add_thing')
    api.add_resource(EditThingResource, '/edit/thing/<int:int_id>', endpoint='handle_edit_thing')
    api.add_resource(CategoryResource, '/categories', endpoint='handle_categories')
    api.add_resource(EditCategoryResource, '/edit/category/<int:int_id>', endpoint='handle_edit_category')
    api.add_resource(StorageResource, '/storages', endpoint='handle_storage')
    api.add_resource(EditStorageResource, '/edit/storage/<int:int_id>', endpoint='handle_edit_storage')
    api.add_resource(ReportResource, '/reports', endpoint='handle_report')
    api.add_resource(TagResource, '/tags', endpoint='handle_tags')
    api.add_resource(EditTagResource, '/edit/tag/<int:int_id>', endpoint='handle_edit_tag')
    api.add_resource(LabelResource, '/label/<int:int_id>', endpoint='handle_label')

    # API Resources
    api.add_resource(categories.CategoriesAPI, '/api/categories', '/api/categories/<int:int_id>')
    api.add_resource(storages.StoragesAPI, '/api/storages', '/api/storages/<int:int_id>')
    api.add_resource(tags.TagsAPI, '/api/tags', '/api/tags/<int:int_id>')
    api.add_resource(things.ThingsAPI, '/api/things', '/api/things/<int:int_id>')
    api.init_app(app)
