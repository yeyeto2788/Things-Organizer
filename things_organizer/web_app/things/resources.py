import logging

import flask
import flask_login
from flask_restful import Resource

from things_organizer.extensions import database
from things_organizer.web_app.categories.models import Category
from things_organizer.web_app.storages.models import Storage
from things_organizer.web_app.things.forms import ThingForm
from things_organizer.web_app.things.models import Thing

logger = logging.getLogger()


class AddThingResource(Resource):
    @flask_login.login_required
    def get(self):
        """Show the `add_thing` template on the site."""

        form = ThingForm()
        current_user = flask_login.current_user.id
        categories = Category.get_user_categories(user_id=current_user)
        form.category.choices = categories
        storages = Storage.get_user_storages(user_id=current_user)
        form.storage.choices = storages

        template_return = flask.render_template("add_thing.html", form=form)

        return flask.Response(template_return, mimetype="text/html")

    @flask_login.login_required
    def post(self):
        """
        This will let the user add a new thing on the db.

        Returns:
            Flask template based on the request method.

        """

        form = ThingForm()
        current_user = flask_login.current_user.id
        categories = Category.get_user_categories(user_id=current_user)
        form.category.choices = categories
        storages = Storage.get_user_storages(user_id=current_user)
        form.storage.choices = storages

        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            unit = form.unit.data
            quantity = form.quantity.data
            user_id = flask_login.current_user.id
            category_id = form.category.data
            storage_id = form.storage.data
            tags = form.tags.data
            thing_obj = Thing(
                name=name,
                description=description,
                user_id=user_id,
                category_id=category_id,
                storage_id=storage_id,
                tags=tags,
                unit=unit,
                quantity=quantity,
            )
            database.session.add(thing_obj)
            database.session.commit()
            flask.flash(f"Stored '{thing_obj.name}'")
            template_return = flask.redirect(flask.url_for("handle_things"))

            return template_return

        template_return = flask.render_template("add_thing.html", form=form)
        return flask.Response(template_return, mimetype="text/html")


class EditThingResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Returns:

        """
        table_object = Thing.query.get_or_404(int_id)
        form = ThingForm(obj=table_object)
        current_user = flask_login.current_user.id
        categories = Category.get_user_categories(user_id=current_user)
        form.category.choices = categories

        storages = Storage.get_user_storages(user_id=current_user)
        form.storage.choices = storages

        selected_storage = table_object.storage_id if table_object.storage_id else 0
        form.storage.default = selected_storage
        form.storage.process_data(selected_storage)

        selected_category = table_object.category_id if table_object.category_id else 0
        form.category.default = selected_category
        form.category.process_data(selected_category)

        if flask_login.current_user != table_object.user:
            flask.abort(403)

        template_return = flask.render_template("edit.html", form=form)
        return flask.Response(template_return, mimetype="text/html")

    @flask_login.login_required
    def post(self, int_id):

        table_object = Thing.query.get_or_404(int_id)
        form = ThingForm(**flask.request.form)

        categories = Category.get_user_categories(user_id=flask_login.current_user.id)
        form.category.choices = categories

        storages = Storage.get_user_storages(user_id=flask_login.current_user.id)
        form.storage.choices = storages

        if flask_login.current_user != table_object.user:
            flask.abort(403)

        if form.validate_on_submit():

            table_object.category_id = form.category.data
            table_object.storage_id = form.storage.data
            table_object.quantity = form.quantity.data
            table_object.unit = form.unit.data
            table_object.name = form.name.data
            table_object.description = form.description.data
            table_object.tags = form.tags.data

            database.session.commit()
            template_return = flask.redirect(flask.url_for("handle_things"))
            return template_return

        template_return = flask.render_template("edit.html", form=form)
        return flask.Response(template_return, mimetype="text/html")


class ThingResource(Resource):
    @flask_login.login_required
    def get(self):
        """
        Handles the showing or not of the things belonging to the user.

        Returns:
            flask template.

        """

        if flask_login.current_user.is_authenticated:
            logger.info("Redirecting to 'things' page.")

            things = Thing.query.filter_by(user_id=flask_login.current_user.id).all()

            if not things:
                things = None

            template_return = flask.render_template("things.html", table_data=things)

        else:
            logger.info("Redirecting to 'login' page.")
            template_return = flask.redirect(flask.url_for("handle_login"))
            flask.session["next_url"] = flask.request.path

        return flask.Response(template_return, mimetype="text/html")


class DeleteThingResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Thing.query.get_or_404(int_id)
        form = ThingForm(obj=table_object)

        flask.flash(f"Please confirm deleting the item '{table_object.name}'.")
        template_return = flask.render_template("confirm_deletion.html", form=form)

        return flask.Response(template_return, mimetype="text/html")

    @flask_login.login_required
    def post(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        table_object = Thing.query.get_or_404(int_id)

        database.session.delete(table_object)
        database.session.commit()
        flask.flash(f"Deleted '{table_object.name}' item")
        template_return = flask.redirect(
            flask.url_for("handle_things", username=flask_login.current_user.username)
        )

        return template_return
