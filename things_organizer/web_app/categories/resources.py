import inspect
import logging
import time

import flask
import flask_login
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from things_organizer.extensions import database
from things_organizer.web_app.categories.forms import CategoryForm
from things_organizer.web_app.categories.models import Category

logger = logging.getLogger()


class CategoryResource(Resource):
    @flask_login.login_required
    def get(self):
        """
        Handles the categories creation and rendering on the page.

        Returns:
            Flask template based on the request method.

        """

        form = CategoryForm()
        categories = Category.query.filter_by(user_id=flask_login.current_user.id).all()

        if not categories:
            categories = None

        template_return = flask.render_template(
            "categories.html", table_data=categories, form=form
        )

        logger.info(
            "** %s - END\t%s **\n",
            inspect.stack()[0][3],
            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        )

        return flask.Response(template_return, mimetype="text/html")

    @flask_login.login_required
    def post(self):
        """

        Returns:

        """

        form = CategoryForm()
        user_id = flask_login.current_user.id

        if form.validate_on_submit():
            name = form.name.data
            category_obj = Category(name=name, user_id=user_id)
            database.session.add(category_obj)
            database.session.commit()
            flask.flash(f"Category {category_obj.name} stored.")

        categories = Category.query.filter_by(user_id=flask_login.current_user.id).all()

        if not categories:
            categories = None

        template_return = flask.render_template(
            "categories.html", table_data=categories, form=form
        )

        return flask.Response(template_return, mimetype="text/html")


class EditCategoryResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        logger.info(
            "** %s - INI\t%s **\n",
            inspect.stack()[0][3],
            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        )

        table_object = Category.query.get_or_404(int_id)
        form = CategoryForm(obj=table_object)
        template_return = flask.render_template("edit.html", form=form)

        if flask_login.current_user.id != table_object.user_id:
            flask.abort(403)

        return flask.Response(template_return, mimetype="text/html")

    @flask_login.login_required
    def post(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Category.query.get_or_404(int_id)
        form = CategoryForm(obj=table_object)

        if form.validate_on_submit():
            form.populate_obj(table_object)  # pylint:disable=E1101

        database.session.commit()

        template_return = flask.redirect(flask.url_for("handle_categories"))
        return template_return


class DeleteCategoryResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Category.query.get_or_404(int_id)
        form = CategoryForm(obj=table_object)

        flask.flash(f"Please confirm deleting the category '{table_object.name}'.")
        template_return = flask.render_template("confirm_deletion.html", form=form)

        return flask.Response(template_return, mimetype="text/html")

    @flask_login.login_required
    def post(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """

        table_object = Category.query.get_or_404(int_id)

        try:
            database.session.delete(table_object)
            database.session.commit()

        except IntegrityError:
            database.session.rollback()  # pylint:disable=E1101
            form = CategoryForm(obj=table_object)

            flask.flash(
                f"You can't delete '{table_object.name}' category "
                f"since it is assigned to an item."
            )
            template_return = flask.Response(
                flask.render_template("confirm_deletion.html", form=form),
                mimetype="text/html",
            )

        else:
            flask.flash(f"Deleted '{table_object.name}' category")
            template_return = flask.redirect(
                flask.url_for(
                    "handle_categories", username=flask_login.current_user.username
                )
            )

        return template_return
