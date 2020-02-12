"""
Main views of the application are declared here.

"""
import time
import inspect

import flask
import flask_login

from sqlalchemy import or_

from things_organizer import app, login_manager, DB
from things_organizer import utils
from things_organizer.forms import LoginForm, SignupForm, ThingForm, ReportForm
from things_organizer.forms import CategoryForm, StorageForm, TagForm
from things_organizer.db import db_models
from things_organizer.labels import QRLabel

from things_organizer.reports import CSV_Report, TXT_Report


_CONTAINER = """
 <div id="content-wrapper">
    <div class="container-fluid">
    {}
    </div>
</div>
"""


@login_manager.user_loader
def load_user(user_id):
    """
    Retrieve the user from the database from a given id.

    Args:
        user_id: id of the user.

    Returns:
        User object.
    """
    return db_models.User.query.get(int(user_id))


@app.route('/about')
def handle_about():
    """
    Shows information about the project.

    Returns:
        Template of the different tools hosted.

    """

    template_return = flask.render_template('about.html')

    return template_return


@app.route('/', endpoint='handle_root')
@app.route('/home', endpoint='handle_root')
def handle_root():
    """
    Main site where user goes to see available tools on the server and the description of them.

    Returns:
        Template of the different tools hosted.

    """
    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    utils.debug("Rendering 'Index' page.")

    template_return = flask.render_template('index.html')

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route('/add_thing', methods=['POST', 'GET'])
@flask_login.login_required
def handle_add_thing():
    """
    This will let the user add a new thing on the db.

    Returns:
        Flask template based on the request method.

    """
    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    form = ThingForm()
    categories = [(cat.id, cat.name) for cat in db_models.Category.query.filter_by(
        user_id=flask_login.current_user.id).all()]
    form.category.choices = categories
    storages = [(s.id, s.name) for s in db_models.Storage.query.filter_by(
        user_id=flask_login.current_user.id).all()]
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
        thing_obj = db_models.Thing(name=name, description=description, user_id=user_id,
                                    category_id=category_id, storage_id=storage_id, tags=tags,
                                    unit=unit, quantity=quantity)
        DB.session.add(thing_obj)
        DB.session.commit()
        flask.flash("Stored '{}'".format(thing_obj.name))
        template_return = flask.redirect(flask.url_for('handle_things'))
    else:
        template_return = flask.render_template('add_thing.html', form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route('/categories', methods=['POST', 'GET'])
@flask_login.login_required
def handle_categories():
    """
    Handles the categories creation and rendering on the page.

    Returns:
        Flask template based on the request method.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    form = CategoryForm()
    user_id = flask_login.current_user.id
    if form.validate_on_submit():
        name = form.name.data
        category_obj = db_models.Category(name=name, user_id=user_id)
        DB.session.add(category_obj)
        DB.session.commit()
        flask.flash("Category {} stored.".format(category_obj.name))

    categories = db_models.Category.query.filter_by(user_id=flask_login.current_user.id).all()
    if not categories:
        categories = None

    template_return = flask.render_template('categories.html', table_data=categories, form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return template_return


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
            table_object = db_models.Category.query.get_or_404(int_id)
            form = CategoryForm(obj=table_object)
            str_redirect = 'handle_categories'
        elif str_to_edit == "storage":
            table_object = db_models.Storage.query.get_or_404(int_id)
            form = StorageForm(obj=table_object)
            str_redirect = 'handle_storage'
        elif str_to_edit == "tag":
            table_object = db_models.Tag.query.get_or_404(int_id)
            form = TagForm(obj=table_object)
            str_redirect = 'handle_tags'
        else:
            table_object = db_models.Thing.query.get_or_404(int_id)
            form = ThingForm(obj=table_object)
            categories = [(cat.id, cat.name) for cat in db_models.Category.query.filter_by(
                user_id=flask_login.current_user.id).all()]
            form.category.choices = categories
            storages = [(s.id, s.name) for s in db_models.Storage.query.filter_by(
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


@app.route('/edit/<string:str_to_edit>/<int:int_id>', methods=['POST', 'GET'])
@flask_login.login_required
def handle_edit(str_to_edit, int_id):
    """
    Edit records depending of the type of table is being requested.

    Args:
        str_to_edit: Type of item to be edited.
        int_id: ID of the item.

    Returns:
        Flask template based on the request method.

    """

    lst_to_edit = ['category', 'storage', 'thing', 'tag']

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    if (str_to_edit in lst_to_edit) and flask_login.current_user.is_authenticated:

        if str_to_edit == "category":
            table_object = db_models.Category.query.get_or_404(int_id)
            form = CategoryForm(obj=table_object)
            str_redirect = 'handle_categories'
        elif str_to_edit == "storage":
            table_object = db_models.Storage.query.get_or_404(int_id)
            form = StorageForm(obj=table_object)
            str_redirect = 'handle_storage'
        elif str_to_edit == "tag":
            table_object = db_models.Tag.query.get_or_404(int_id)
            form = TagForm(obj=table_object)
            str_redirect = 'handle_tags'
        else:
            table_object = db_models.Thing.query.get_or_404(int_id)
            form = ThingForm(obj=table_object)

            categories = [(cat.id, cat.name) for cat in db_models.Category.query.filter_by(
                user_id=flask_login.current_user.id).all()]

            form.category.choices = categories

            storages = [(s.id, s.name) for s in db_models.Storage.query.filter_by(
                user_id=flask_login.current_user.id).all()]

            form.storage.choices = storages
            str_redirect = 'handle_things'

            if flask_login.current_user != table_object.user:
                flask.abort(403)

        if form.validate_on_submit():

            if str_to_edit == 'thing':
                table_object.category_id = form.category.data
                table_object.storage_id = form.storage.data
                table_object.quantity = form.quantity.data
                table_object.unit = form.unit.data
                table_object.name = form.name.data
                table_object.description = form.description.data

            else:
                form.populate_obj(table_object)
            DB.session.commit()
            template_return = flask.redirect(flask.url_for(str_redirect))
        else:
            template_return = flask.render_template('edit.html', form=form)
    else:
        template_return = flask.redirect(flask.url_for('handle_root'))

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route('/label/<int:int_id>', methods=['POST', 'GET'])
@flask_login.login_required
def handle_label(int_id):
    """
    Generate the label for a given item.

    Args:
        int_id: ID of the item

    Returns:
        Flask template based on the request method.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    thing = db_models.Thing.query.filter_by(user_id=flask_login.current_user.id, id=int_id).first()

    storage = db_models.Storage.query.filter_by(id=thing.storage_id).first()

    if thing:
        label = QRLabel(thing.name, thing.description, storage.name, storage.location)
        label.generate_label()

        template_return = flask.send_from_directory(
            label.file_directory, label.file_name, as_attachment=True)
        flask.flash("Label '{}' generated.".format(label.file_name))

    else:
        template_return = flask.redirect(flask.url_for('handle_things'))

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route("/login", methods=['POST', 'GET'])
def handle_login():
    """
    Handles the login page based on the request method, if request is POST it will check user
    existence on the database. If the request is GET it will just send the login page.

    Returns:
        Flask template based on the request method.

    """
    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    form = LoginForm()
    if form.validate_on_submit():
        user_obj = db_models.User.get_by_username(form.username.data)
        if user_obj is not None and user_obj.check_password(form.password.data):
            flask_login.login_user(user_obj, form.remember_me.data)
            flask.flash("Welcome, {}!.".format(user_obj.username))
            flask_template = flask.redirect(flask.request.args.get('next') or flask.url_for(
                'handle_root', username=user_obj.username))
        else:
            flask.flash('ERROR:Incorrect username or password.')
            flask_template = flask.render_template("login.html", form=form)
    else:
        flask_template = flask.render_template("login.html", form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


@app.route('/logout')
def handle_logout():
    """
    Remove the user's flask session.

    Returns:
        It will redirect the user to home.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    # Remove the username from the session if it's there
    flask_login.logout_user()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return flask.redirect(flask.url_for('handle_root'))


@app.route("/search", methods=['POST'])
@app.route("/search.html", methods=['POST'])
@flask_login.login_required
def handle_search():
    """
    This function is meant to be used for searching a text within the database.

    Returns:
        Flask template.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    if flask_login.current_user.is_authenticated:

        form_text = flask.request.form.get('search-text')
        template_text = "Results for <b>'{}'</b>. ".format(form_text)
        print(form_text)

        if form_text.startswith('thing:'):
            search_txt = form_text.split(':')[1].lstrip()
            print(search_txt)
            things = db_models.Thing.query.filter(
                db_models.User.id == flask_login.current_user.id, or_(
                    db_models.Thing.name.contains('{}%'.format(search_txt)),
                    db_models.Thing.description.contains('{}%'.format(search_txt)))
                ).all()

            if things:
                template_text += 'Found <b>{}</b> items.\n\n'.format(len(things))

                for int_index, thing in enumerate(things):
                    int_index += 1
                    template_text += '<b>Item {:02}</b>\n'.format(int_index)
                    template_text += '<b>Name:</b> {}\n'.format(str(thing.name))
                    template_text += '<b>Description:</b> {}\n'.format(str(thing.description))
                    storage = db_models.Storage.query.filter_by(id=thing.storage_id).first()
                    template_text += '<b>Storage:</b> {}\n'.format(storage.name)
                    template_text += '<b>Location:</b> {}\n'.format(storage.location)
                    category = db_models.Category.query.filter_by(id=thing.category_id).first()
                    template_text += '<b>Category:</b> {}\n\n'.format(category.name)

                template_text = template_text.replace('\n', '<br>')
            else:
                template_text += "<b>No items found.</b>"

        else:
            template_text += "<b>No items found.</b>"

        container = """
        <div class="container-fluid lead">
        {}
        <p class="lead" align="center">You can <a href="javascript:history.back()">
        go back</a>
        to the previous page, or <a href="/home">home</a>.</p>
        </div>""".format(template_text)
        flask_template = flask.render_template('_blank.html', str_to_display=str(container))

    else:
        utils.debug("Redirecting to 'login' page.")
        flask_template = flask.redirect(flask.url_for('handle_login'))
        flask.session['next_url'] = flask.request.path

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


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


@app.route('/storages', methods=['POST', 'GET'])
@flask_login.login_required
def handle_storage():
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
        storage_obj = db_models.Storage(name=name, location=location, user_id=user_id)
        DB.session.add(storage_obj)
        DB.session.commit()
        flask.flash("Storage {} stored with location {}.".format(storage_obj.name,
                                                                 storage_obj.location))
    storages = db_models.Storage.query.filter_by(user_id=user_id).all()
    if not storages:
        storages = None

    template_return = flask.render_template('storages.html', table_data=storages, form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return template_return


@app.route('/register', methods=['POST', 'GET'])
def handle_register():
    """
    Register the user on the db, if the request it type `GET` it will
    return the form to be filled and then send it through a `POST`
    request.

    Returns:
        Flask template '_blank' modified based on the request.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    form = SignupForm()
    if form.validate_on_submit() and flask.request.method == "POST":
        user_obj = db_models.User(email=form.email.data,
                                  username=form.username.data,
                                  password=form.password.data,)
        DB.session.add(user_obj)
        DB.session.commit()
        flask.flash('Welcome, {}! Please login.'.format(user_obj.username))
        flask_template = flask.redirect(flask.url_for('handle_login'))
    else:
        if flask.request.method == "POST":
            flask.flash('ERROR: Hhmm, seems like there was an error registering you account.')

        flask_template = flask.render_template("register.html", form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


@app.route('/reports', methods=['POST', 'GET'])
@flask_login.login_required
def handle_report():
    """
    Use for generating the reports through a page.

    Returns:
        Flask template '_blank' modified based on the request.

    """
    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    form = ReportForm()
    report_types = [(1, 'CSV (.csv)'), (2, 'TXT (.txt)')]
    form.report_type.choices = report_types
    data_types = [(1, 'All items'), (2, 'All items by Category'), (3, 'All items by Storage')]
    form.data_type.choices = data_types
    categories = [(cat.id, cat.name) for cat in db_models.Category.query.filter_by(
        user_id=flask_login.current_user.id).all()]
    form.category.choices = categories
    storages = [(s.id, s.name) for s in db_models.Storage.query.filter_by(
        user_id=flask_login.current_user.id).all()]
    form.storage.choices = storages

    if form.validate_on_submit():
        report_type = form.report_type.data
        data_type = form.data_type.data
        category = form.category.data
        storage = form.storage.data

        report_name = '{}'.format(str(int(time.time())))
        print(report_name)

        if report_type == 1:
            report = CSV_Report(report_name, flask_login.current_user.id)
        else:
            report = TXT_Report(report_name, flask_login.current_user.id)

        if data_type == 1:
            report.get_all_things()
        else:
            if data_type == 2:
                report.get_by_category(category)
            else:
                report.get_by_storage(storage)

        template_return = flask.send_from_directory(report.file_directory,
                                                    report.file_name,
                                                    as_attachment=True)
    else:
        template_return = flask.render_template('reports.html', form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route("/tags", methods=['POST', 'GET'])
@app.route("/tags.html", methods=['POST', 'GET'])
@flask_login.login_required
def handle_tags():
    """
    Handles the showing or not of the tags on the system.

    Returns:
        flask template.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    form = TagForm()
    if form.validate_on_submit():
        name = form.name.data
        tag_obj = db_models.Tag(name=name)
        DB.session.add(tag_obj)
        DB.session.commit()
        flask.flash("Tag {} stored.".format(tag_obj.name))
    tags = db_models.Tag.query.filter().all()

    if not tags:
        tags = None

    template_return = flask.render_template('tags.html', table_data=tags, form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route("/things", methods=['GET'])
@app.route("/things.html", methods=['GET'])
@flask_login.login_required
def handle_things():
    """
    Handles the showing or not of the things belonging to the user.

    Returns:
        flask template.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    if flask_login.current_user.is_authenticated:
        utils.debug("Redirecting to 'things' page.")

        things = db_models.Thing.query.filter_by(user_id=flask_login.current_user.id).all()

        if not things:
            things = None

        flask_template = flask.render_template('things.html', table_data=things)

    else:
        utils.debug("Redirecting to 'login' page.")
        flask_template = flask.redirect(flask.url_for('handle_login'))
        flask.session['next_url'] = flask.request.path

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


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
