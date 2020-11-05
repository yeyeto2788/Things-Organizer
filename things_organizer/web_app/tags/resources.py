import inspect
import time

import flask
import flask_login
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from things_organizer import utils
from things_organizer.extensions import database
from things_organizer.web_app.tags.forms import TagForm
from things_organizer.web_app.tags.models import Tag


class TagResource(Resource):

    @flask_login.login_required
    def get(self):
        """
        Handles the showing or not of the tags on the system.

        Returns:
            flask template.

        """

        form = TagForm()
        tags = Tag.query.filter().all()

        if not tags:
            tags = None

        template_return = flask.render_template('tags.html', table_data=tags,
                                                form=form)

        utils.debug(
            "** {} - END\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )

        return flask.Response(template_return, mimetype='text/html')

    @flask_login.login_required
    def post(self):
        """
        Handles the showing or not of the tags on the system.

        Returns:
            flask template.

        """

        form = TagForm()

        if form.validate_on_submit():
            name = form.name.data
            tag_obj = Tag(name=name)
            database.session.add(tag_obj)
            database.session.commit()
            flask.flash("Tag {} stored.".format(tag_obj.name))
        tags = Tag.query.filter().all()

        if not tags:
            tags = None

        template_return = flask.render_template(
            'tags.html',
            table_data=tags,
            form=form
        )

        utils.debug(
            "** {} - END\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )

        return flask.Response(template_return, mimetype='text/html')


class EditTagResource(Resource):

    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Tag.query.get_or_404(int_id)
        form = TagForm(obj=table_object)
        template_return = flask.render_template('edit.html', form=form)

        return template_return

    @flask_login.login_required
    def post(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Tag.query.get_or_404(int_id)
        form = TagForm(obj=table_object)

        if form.validate_on_submit():
            form.populate_obj(table_object)  # pylint:disable=E1101

        database.session.commit()

        template_return = flask.redirect(flask.url_for('handle_categories'))
        return flask.Response(template_return, mimetype='text/html')


class DeleteTagResource(Resource):

    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Tag.query.get_or_404(int_id)
        form = TagForm(obj=table_object)

        flask.flash(
            "Please confirm deleting the tag '{}'.".format(table_object.name)
        )
        template_return = flask.render_template(
            "confirm_deletion.html",
            form=form
        )

        return flask.Response(template_return, mimetype='text/html')

    @flask_login.login_required
    def post(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Tag.query.get_or_404(int_id)

        try:
            database.session.delete(table_object)
            database.session.commit()

        except IntegrityError:
            database.session.rollback()  # pylint:disable=E1101
            form = TagForm(obj=table_object)

            flask.flash(
                f"You can't delete '{table_object.name}' tag "
                f"since it is assigned to an item."
            )
            template_return = flask.Response(
                flask.render_template("confirm_deletion.html", form=form),
                mimetype='text/html')

        else:
            flask.flash("Deleted '{}' tag".format(table_object.name))
            template_return = flask.redirect(
                flask.url_for('handle_tags',
                              username=flask_login.current_user.username))

        return template_return
