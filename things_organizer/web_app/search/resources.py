import logging

import flask
import flask_login
from flask_restful import Resource
from sqlalchemy import or_

from things_organizer.web_app.categories.models import Category
from things_organizer.web_app.storages.models import Storage
from things_organizer.web_app.things.models import Thing
from things_organizer.web_app.users.models import User

logger = logging.getLogger()


class SearchResource(Resource):
    @flask_login.login_required
    def get(self):
        """
        This function is meant to be used for searching a text within the
        database.

        Returns:
            Flask template.

        """

        if flask_login.current_user.is_authenticated:

            form_text = flask.request.form.get("search-text")
            template_text = f"Results for <b>'{form_text}'</b>. "
            print(form_text)

            if form_text.startswith("thing:"):
                search_txt = form_text.split(":")[1].lstrip()
                print(search_txt)
                things = Thing.query.filter(
                    User.id == flask_login.current_user.id,
                    or_(
                        Thing.name.contains(f"{search_txt}%"),
                        Thing.description.contains(f"{search_txt}%"),
                    ),
                ).all()

                if things:
                    template_text += f"Found <b>{len(things)}</b> items.\n\n"

                    for int_index, thing in enumerate(things):
                        int_index += 1
                        template_text += f"<b>Item {int_index:02}</b>\n"
                        template_text += f"<b>Name:</b> {str(thing.name)}\n"
                        template_text += (
                            f"<b>Description:</b> {str(thing.description)}\n"
                        )

                        storage = Storage.query.filter_by(id=thing.storage_id).first()
                        template_text += f"<b>Storage:</b> {storage.name}\n"
                        template_text += f"<b>Location:</b> {storage.location}\n"
                        category = Category.query.filter_by(
                            id=thing.category_id
                        ).first()
                        template_text += f"<b>Category:</b> {category.name}\n\n"

                    template_text = template_text.replace("\n", "<br>")

                else:
                    template_text += "<b>No items found.</b>"

            else:
                template_text += "<b>No items found.</b>"

            container = f"""
                <div class="container-fluid lead">
                {template_text}
                <p class="lead" align="center">
                You can <a href="javascript:history.back()">go back</a>
                to the previous page, or <a href="/home">home</a>.
                </p>
                </div>"""

            flask_template = flask.render_template(
                "_blank.html", str_to_display=str(container)
            )

        else:
            logger.info("Redirecting to 'login' page.")
            flask_template = flask.redirect(flask.url_for("handle_login"))
            flask.session["next_url"] = flask.request.path

        return flask.Response(flask_template, mimetype="text/html")
