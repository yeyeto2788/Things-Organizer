"""
Flask server run
"""
import os

from waitress import serve

from things_organizer.app import create_app


def run(debug: bool = False):
    """
    Serves a flask application using waitress.

        Args:
            debug: enables debug mode or not. Default is False so it is disabled.

    """
    app = create_app(debug=debug)

    if debug is False:
        app.run(
            host='127.0.0.1',
            port=os.getenv('APP_PORT', 8080)
        )
    else:
        serve(
            app,
            port=os.getenv('APP_PORT', 8080),
            threads=10,
        )


if __name__ == '__main__':
    debug_string = os.getenv("DEBUG")
    positive_options = [
        'true', '1', 't', 'y',
        'yes', 'yeah', 'yup', 'certainly',
        'uh-huh'
    ]
    debug = False

    if debug_string.lower() in positive_options:
        debug = True

    run(debug)
