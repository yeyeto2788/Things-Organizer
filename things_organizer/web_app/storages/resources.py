import inspect
import time

import flask
import flask_login
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from things_organizer import utils
from things_organizer.extensions import database
from things_organizer.web_app.storages.forms import StorageForm
from things_organizer.web_app.storages.models import Storage


class StorageResource(Resource):
    @flask_login.login_required
    def get(self):
        """
        Handles the storage creation and rendering on the page.

        Returns:
            Flask template based on the request method.

        """

        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        form = StorageForm()
        storages = Storage.query.filter_by(user_id=flask_login.current_user.id).all()

        if not storages:
            storages = None

        template_return = flask.render_template('storages.html', table_data=storages, form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        return flask.Response(template_return, mimetype='text/html')

    @flask_login.login_required
    def post(self):
        """
        Handles the storage creation and rendering on the page.

        Returns:
            Flask template based on the request method.

        """

        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        form = StorageForm()
        user_id = flask_login.current_user.id

        if form.validate_on_submit():
            name = form.name.data
            location = form.location.data
            storage_obj = Storage(name=name, location=location, user_id=user_id)
            database.session.add(storage_obj)
            database.session.commit()
            flask.flash("Storage {} stored with location {}.".format(storage_obj.name,
                                                                     storage_obj.location))
        storages = Storage.query.filter_by(user_id=user_id).all()

        if not storages:
            storages = None

        template_return = flask.render_template('storages.html', table_data=storages, form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        return flask.Response(template_return, mimetype='text/html')


class EditStorageResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        table_object = Storage.query.get_or_404(int_id)
        form = StorageForm(obj=table_object)
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
        table_object = Storage.query.get_or_404(int_id)
        form = StorageForm(obj=table_object)

        if form.validate_on_submit():
            form.populate_obj(table_object)

        database.session.commit()

        template_return = flask.redirect(flask.url_for('handle_storage'))
        return template_return

class DeleteStorageResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """

        Args:
            int_id:

        Returns:

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        table_object = Storage.query.get_or_404(int_id)
        form = StorageForm(obj=table_object)

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
        table_object = Storage.query.get_or_404(int_id)

        try:
            database.session.delete(table_object)
            database.session.commit()

        except IntegrityError:
            database.session.rollback()
            form = StorageForm(obj=table_object)

            flask.flash("You can't delete '{}' category since it is assigned to an item.".format(table_object.name))
            template_return = flask.Response(flask.render_template("confirm_deletion.html", form=form), mimetype='text/html')

        else:
            flask.flash("Deleted '{}' storage".format(table_object.name))
            template_return = flask.redirect(flask.url_for('handle_storage', username=flask_login.current_user.username))

        return template_return
