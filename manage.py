#!/usr/bin/python3
"""
Flask server run
"""
import os

from flask_migrate import MigrateCommand
from flask_script import Manager
from waitress import serve

from things_organizer.app import create_app

app = create_app()
manager = Manager(app, with_default_commands=False)
manager.add_command('db', MigrateCommand)


@manager.option(
    '-d', '--debug',
    dest='debug', help="Run server on debug mode or not",
    default=False
)
def runserver(debug):
    """Run the server application"""
    if debug is True:
        app.run(
            host='127.0.0.1',
            port=os.getenv('APP_PORT', 8080)
        )
    else:
        serve(
            app,
            host='0.0.0.0',
            port=os.getenv('APP_PORT', 8080),
            threads=10,
        )


if __name__ == '__main__':
    manager.run()
