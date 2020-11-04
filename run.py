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
    app = create_app(True)
    serve(
        app,
        port=os.getenv('APP_PORT', 8080)
    )


if __name__ == '__main__':
    run()
