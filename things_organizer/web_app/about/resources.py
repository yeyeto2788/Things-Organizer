import flask
from flask_restful import Resource


class AboutResource(Resource):
    def get(self):
        """
        Shows information about the project.

        Returns:
            Template of the different tools hosted.

        """

        template_return = flask.render_template("about.html")

        return flask.Response(template_return, mimetype="text/html")
