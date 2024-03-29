import flask
import flask_login
from flask_restful import Resource

from things_organizer.labels import QRLabel
from things_organizer.web_app.storages.models import Storage
from things_organizer.web_app.things.models import Thing


class LabelResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """
        Generate the label for a given item.

        Args:
            int_id: ID of the item

        Returns:
            Flask template based on the request method.

        """

        thing = Thing.query.filter_by(
            user_id=flask_login.current_user.id, id=int_id
        ).first()

        storage = Storage.query.filter_by(id=thing.storage_id).first()

        if thing:
            label = QRLabel(
                thing.name, thing.description, storage.name, storage.location
            )
            label.generate_label()

            template_return = flask.send_from_directory(
                label.file_directory, label.file_name, as_attachment=True
            )
            flask.flash(f"Label '{label.file_name}' generated.")

            return template_return

        template_return = flask.redirect(flask.url_for("handle_things"))
        return flask.Response(template_return, mimetype="text/html")
