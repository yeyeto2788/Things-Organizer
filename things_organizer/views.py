"""
Main views of the application are declared here.

"""
import inspect
import time

import flask
import flask_login

import things_organizer.categories.models
import things_organizer.common.models
import things_organizer.storages.models
import things_organizer.tags.models
import things_organizer.things.models
from things_organizer import app, DB
from things_organizer import utils
from things_organizer.categories.forms import CategoryForm
from things_organizer.storages.forms import StorageForm
from things_organizer.tags.forms import TagForm
from things_organizer.things.forms import ThingForm

@app.route('/delete/<string:str_to_edit>/<int:int_id>', methods=['POST', 'GET'])
@flask_login.login_required
def handle_delete(str_to_edit, int_id):
    """
    Edit records depending of the type of table is being requested.

    Args:
        str_to_edit:
        int_id:

    Returns:
        Flask template based on the request method.

    """

    lst_to_edit = ['category', 'storage', 'thing', 'tag']

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    if (str_to_edit in lst_to_edit) and flask_login.current_user.is_authenticated:

        if str_to_edit == "category":
            table_object = things_organizer.categories.models.Category.query.get_or_404(int_id)
            form = CategoryForm(obj=table_object)
            str_redirect = 'handle_categories'
        elif str_to_edit == "storage":
            table_object = things_organizer.storages.models.Storage.query.get_or_404(int_id)
            form = StorageForm(obj=table_object)
            str_redirect = 'handle_storage'
        elif str_to_edit == "tag":
            table_object = things_organizer.tags.models.Tag.query.get_or_404(int_id)
            form = TagForm(obj=table_object)
            str_redirect = 'handle_tags'
        else:
            table_object = things_organizer.things.models.Thing.query.get_or_404(int_id)
            form = ThingForm(obj=table_object)
            categories = [(cat.id, cat.name) for cat in things_organizer.categories.models.Category.query.filter_by(
                user_id=flask_login.current_user.id).all()]
            form.category.choices = categories
            storages = [(s.id, s.name) for s in things_organizer.storages.models.Storage.query.filter_by(
                user_id=flask_login.current_user.id).all()]
            form.storage.choices = storages
            str_redirect = 'handle_things'

            if flask_login.current_user != table_object.user:
                flask.abort(403)

        if flask.request.method == "POST":
            DB.session.delete(table_object)
            DB.session.commit()
            flask.flash("Deleted '{}' {}".format(table_object.name, str_to_edit))
            template_return = flask.redirect(flask.url_for(
                str_redirect, username=flask_login.current_user.username))
        else:
            flask.flash("Please confirm deleting the {} '{}'.".format(
                str_to_edit, table_object.name))
            template_return = flask.render_template("confirm_deletion.html", form=form)

    else:
        template_return = flask.redirect(flask.url_for('handle_root'))

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route('/settings', methods=['POST', 'GET'])
@flask_login.login_required
def handle_settings():
    """
    Set all setting of the application (Still under development).

    Returns:
        Flask template based on the request.

    """

    template_return = flask.render_template('settings.html')

    return template_return


@app.errorhandler(404)
def page_not_found(error):
    """
    Function for handling all bad requests to the application.

    Args:
        error:

    Returns:
        Template for 404 error code.

    """

    return flask.render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(error):
    """
    Function for handling all forbidden requests to the application.

    Args:
        error:

    Returns:
        Template for 403 error code.

    """
    return flask.render_template('403.html'), 403
