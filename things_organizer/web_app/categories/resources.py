import inspect
import time

import flask
import flask_login
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from things_organizer import utils
from things_organizer.web_app.categories.forms import CategoryForm
from things_organizer.web_app.categories.models import Category
from things_organizer.extensions import database


class CategoryResource(Resource):
    @flask_login.login_required
    def get(self):
        """
        Handles the categories creation and rendering on the page.

        Returns:
            Flask template based on the request method.

        """

        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        form = CategoryForm()
        categories = Category.query.filter_by(user_id=flask_login.current_user.id).all()

        if not categories:
            categories = None

        template_return = flask.render_template('categories.html', table_data=categories, form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        return flask.Response(template_return, mimetype='text/html')

    @flask_login.login_required
    def post(self):
        """

        Returns:

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        form = CategoryForm()
        user_id = flask_login.current_user.id

        if form.validate_on_submit():
            name = form.name.data
            category_obj = Category(name=name, user_id=user_id)
            database.session.add(category_obj)
            database.session.commit()
            flask.flash("Category {} stored.".format(category_obj.name))

        categories = Category.query.filter_by(user_id=flask_login.current_user.id).all()

        if not categories:
            categories = None

        template_return = flask.render_template('categories.html', table_data=categories, form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        return flask.Response(template_return, mimetype='text/html')


class EditCategoryResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        table_object = Category.query.get_or_404(int_id)
        form = CategoryForm(obj=table_object)
        template_return = flask.render_template('edit.html', form=form)

        if flask_login.current_user.id != table_object.user_id:
            flask.abort(403)

        return flask.Response(template_return, mimetype='text/html')

    @flask_login.login_required
    def post(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        table_object = Category.query.get_or_404(int_id)
        form = CategoryForm(obj=table_object)

        if form.validate_on_submit():
            form.populate_obj(table_object)

        database.session.commit()

        template_return = flask.redirect(flask.url_for('handle_categories'))
        return template_return


class DeleteCategoryResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        table_object = Category.query.get_or_404(int_id)
        form = CategoryForm(obj=table_object)

        flask.flash("Please confirm deleting the category '{}'.".format(table_object.name))
        template_return = flask.render_template("confirm_deletion.html", form=form)

        return flask.Response(template_return, mimetype='text/html')

    @flask_login.login_required
    def post(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        table_object = Category.query.get_or_404(int_id)

        try:
            database.session.delete(table_object)
            database.session.commit()

        except IntegrityError:
            database.session.rollback()  # pylint:disable=E1101
            form = CategoryForm(obj=table_object)

            flask.flash("You can't delete '{}' category since it is assigned to an item.".format(table_object.name))
            template_return = flask.Response(flask.render_template("confirm_deletion.html", form=form), mimetype='text/html')

        else:
            flask.flash("Deleted '{}' category".format(table_object.name))
            template_return = flask.redirect(
                flask.url_for('handle_categories', username=flask_login.current_user.username))

        return template_return
