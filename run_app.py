"""
Simple script to manage server actions through CLI

"""
import os
import flask

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from waitress import serve

from things_organizer import app, DB
from things_organizer.utils import DB_PATH

# TODO: Put all application related configuration into a file.
config = {'ip': '0.0.0.0', 'port': 8080}

# Generate a new Key with os.urandom(16) if you want to change it.
app.secret_key = '3ZX\xb336\x15\x82/\xd5N1O\n\x9f\x8a'


migrate = Migrate(app, DB)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """
    Creates database tables from sqlalchemy models

    """
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    DB.create_all()


@manager.command
def drop_db():
    """
    Drop all data on database.

    """
    if prompt_bool("Are you sure you want to lose all your data"):
        DB.drop_all()


@manager.command
def recreate_db():
    """
    Recreates database tables (same as issuing 'drop' and then 'create')

    """
    drop_db()
    create_db()


@manager.command
def run_development():
    """
    Runs the server on debug mode.

    """
    app.run(host=config['ip'], port=config['port'], threaded=True, debug=True)


@manager.command
def run_production():
    """
    Runs the server as WSGI.

    """
    serve(app, listen='{}:{}'.format(config['ip'], config['port']))\


@manager.command
def show_endpoints():
    """
    Show all possible endpoints where requests can be done.

    """

    print('\nThis are the possible endpoints of the application:\n')

    rules = [rule for rule in app.url_map._rules]

    for rule in rules:

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        try:
            rule_url = flask.url_for(rule.endpoint)
            rule_methods = ','.join(rule.methods)

            print('{:30s} - {:50s}'.format(rule_methods, rule_url))
        except Exception as exerror:
            print('{:30s} - {:50s}'.format(rule_methods, rule.endpoint))


if __name__ == '__main__':
    manager.run()
