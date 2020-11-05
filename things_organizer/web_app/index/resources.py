import logging

import flask
from flask_restful import Resource

logger = logging.getLogger()


class HomeResource(Resource):

    def get(self):
        """Main site where user goes to see available tools on the server
        and the description of them.

        Returns:
            Template of the different tools hosted.

        """

        logger.info("Rendering 'Index' page.")

        template_return = flask.render_template('index.html')

        return flask.Response(template_return, mimetype='text/html')
