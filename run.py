"""
Flask server run
"""
import os

from waitress import serve

from things_organizer.app import create_app
from things_organizer.utils import str_to_bln


def run(debug: bool = False):
    """
    Serves a flask application using waitress.

        Args:
            debug: enables debug mode or not. Default is False so it is disabled.

    """
    app = create_app(debug=debug)

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
    debug_string = os.getenv("DEBUG", "false")
    debug = False

    if str_to_bln(debug_string):
        debug = True

    run(debug)
