import inspect
import time

import flask
import flask_login
from flask_restful import Resource
from sqlalchemy import or_

from things_organizer import utils
from things_organizer.web_app.categories.models import Category
from things_organizer.web_app.storages.models import Storage
from things_organizer.web_app.things.models import Thing
from things_organizer.web_app.users.models import User


class SearchResource(Resource):

    @flask_login.login_required
    def get(self):
        """
        This function is meant to be used for searching a text within the database.

        Returns:
            Flask template.

        """

        if flask_login.current_user.is_authenticated:

            form_text = flask.request.form.get('search-text')
            template_text = "Results for <b>'{}'</b>. ".format(form_text)
            print(form_text)

            if form_text.startswith('thing:'):
                search_txt = form_text.split(':')[1].lstrip()
                print(search_txt)
                things = Thing.query.filter(
                    User.id == flask_login.current_user.id, or_(
                        Thing.name.contains('{}%'.format(search_txt)),
                        Thing.description.contains('{}%'.format(search_txt)))
                ).all()

                if things:
                    template_text += 'Found <b>{}</b> items.\n\n'.format(
                        len(things))

                    for int_index, thing in enumerate(things):
                        int_index += 1
                        template_text += '<b>Item {:02}</b>\n'.format(
                            int_index)
                        template_text += '<b>Name:</b> {}\n'.format(
                            str(thing.name))
                        template_text += '<b>Description:</b> {}\n'.format(
                            str(thing.description))
                        storage = Storage.query.filter_by(
                            id=thing.storage_id).first()
                        template_text += '<b>Storage:</b> {}\n'.format(
                            storage.name)
                        template_text += '<b>Location:</b> {}\n'.format(
                            storage.location)
                        category = Category.query.filter_by(
                            id=thing.category_id).first()
                        template_text += '<b>Category:</b> {}\n\n'.format(
                            category.name)

                    template_text = template_text.replace('\n', '<br>')

                else:
                    template_text += "<b>No items found.</b>"

            else:
                template_text += "<b>No items found.</b>"

            container = """
                <div class="container-fluid lead">
                {}
                <p class="lead" align="center">
                You can <a href="javascript:history.back()">go back</a>
                to the previous page, or <a href="/home">home</a>.
                </p>
                </div>""".format(template_text)
            flask_template = flask.render_template(
                '_blank.html',
                str_to_display=str(
                    container)
            )

        else:
            utils.debug("Redirecting to 'login' page.")
            flask_template = flask.redirect(flask.url_for('handle_login'))
            flask.session['next_url'] = flask.request.path

        utils.debug(
            "** {} - END\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )
        return flask.Response(flask_template, mimetype='text/html')
