import inspect
import time

import flask
from flask_restful import Resource

from things_organizer import utils


class HomeResource(Resource):
    def get(self):
        """Main site where user goes to see available tools on the server
        and the description of them.

        Returns:
            Template of the different tools hosted.

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        utils.debug("Rendering 'Index' page.")

        template_return = flask.render_template('index.html')

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        return flask.Response(template_return, mimetype='text/html')
