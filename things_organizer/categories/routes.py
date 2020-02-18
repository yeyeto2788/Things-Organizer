import inspect
import time

import flask
import flask_login
from flask_restful import Resource

from things_organizer import utils
from things_organizer.categories.forms import CategoryForm
from things_organizer.categories.models import Category
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
        return flask.Response(template_return, mimetype='text/html')
