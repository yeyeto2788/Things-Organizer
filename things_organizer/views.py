"""
Main views of the application are declared here.

"""
import time
import inspect

import flask
import flask_login

from things_organizer import app, login_manager, DB
from things_organizer import utils
from things_organizer.forms import LoginForm, SignupForm, ThingForm, CategoryForm, StorageForm, TagForm
from things_organizer.data_management import common, user, tag, category, storage
from things_organizer.db import db_models


_CONTAINER = """
 <div id="content-wrapper">
    <div class="container-fluid">
    {}
    </div>
</div>
"""


@login_manager.user_loader
def load_user(userid):
    return db_models.User.query.get(int(userid))


@app.route('/')
@app.route('/home')
def root():
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
    categories = [(cat.id, cat.name) for cat in db_models.Category.query.all()]
    form.category.choices = categories
    storages = [(s.id, s.name) for s in db_models.Storage.query.all()]
    form.storage.choices = storages

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        user_id = flask_login.current_user.id
        category_id = form.category.data
        storage_id = form.storage.data
        tags = form.tags.data
        thing_obj = db_models.Thing(name=name, description=description, user_id=user_id,
                                    category_id=category_id, storage_id=storage_id, tags=tags)
        DB.session.add(thing_obj)
        DB.session.commit()
        flask.flash("Stored '{}'".format(thing_obj.description))
        template_return = flask.redirect(flask.url_for('handle_things'))
    else:
        template_return = flask.render_template('add_thing.html', form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route('/edit/<string:str_to_edit>/<int:int_id>', methods=['POST', 'GET'])
@flask_login.login_required
def handle_edit(str_to_edit, int_id):
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
            categories = [(cat.id, cat.name) for cat in db_models.Category.query.all()]
            form.category.choices = categories
            storages = [(s.id, s.name) for s in db_models.Storage.query.all()]
            form.storage.choices = storages
            str_redirect = 'handle_things'

            if flask_login.current_user != table_object.user:
                flask.abort(403)

        if form.validate_on_submit():
            # TODO: Fix population of thing
            if str_to_edit == 'thing':
                table_object.category_id = form.category.data
                table_object.storage_id = form.storage.data
                table_object.user_id = flask_login.current_user.id

            form.populate_obj(table_object)
            DB.session.commit()
            template_return = flask.redirect(flask.url_for(str_redirect))
        else:
            template_return = flask.render_template('edit.html', form=form)
    else:
        template_return = flask.redirect(flask.url_for('root'))

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
            categories = [(cat.id, cat.name) for cat in db_models.Category.query.all()]
            form.category.choices = categories
            storages = [(s.id, s.name) for s in db_models.Storage.query.all()]
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
        template_return = flask.redirect(flask.url_for('root'))

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
                'root', username=user_obj.username))
        else:
            flask.flash('Incorrect username or password.')
            flask_template = flask.render_template("login.html", form=form)
    else:
        flask_template = flask.render_template("login.html", form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


@app.route('/logout')
def handle_logout():
    """
    Remove the user sessionkey from database and remove email from the flask session.

    Returns:
        It will redirect the user to home.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    # Remove the username from the session if it's there
    flask_login.logout_user()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return flask.redirect(flask.url_for('root'))


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
    if form.validate_on_submit():
        name = form.name.data
        category_obj = db_models.Category(name=name)
        DB.session.add(category_obj)
        DB.session.commit()
        flask.flash("Category {} stored.".format(category_obj.name))

    categories = db_models.Category.query.filter().all()
    if not categories:
        categories = None

    template_return = flask.render_template('categories.html', table_data=categories, form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return template_return


@app.route("/search", methods=['POST'])
@app.route("/search.html", methods=['POST'])
@flask_login.login_required
def handle_search():
    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    if flask_login.current_user.is_authenticated:

        form_text = flask.request.form.get('search-text')
        template_text = "Results for '{}' > ".format(form_text)
        print(form_text)

        if form_text.startswith('thing:'):
            search_txt = form_text.split(':')[1].lstrip()
            things = db_models.Thing.query.filter_by(
                user_id=flask_login.current_user.id).filter(
                db_models.Thing.name.like("%" + search_txt + "%")).first()

            if things:
                template_text += str(things)
            else:
                template_text += "NOT FOUND"

        flask_template = flask.render_template('_blank.html', str_to_display=str(template_text))

    else:
        utils.debug("Redirecting to 'login' page.")
        flask_template = flask.redirect(flask.url_for('handle_login'))
        flask.session['next_url'] = flask.request.path

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


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
    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        storage_obj = db_models.Storage(name=name, location=location)
        DB.session.add(storage_obj)
        DB.session.commit()
        flask.flash("Storage {} stored with location {}.".format(storage_obj.name,
                                                                 storage_obj.location))
    storages = db_models.Storage.query.filter().all()
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
    if form.validate_on_submit():
        user_obj = db_models.User(email=form.email.data,
                                  username=form.username.data,
                                  password=form.password.data,)
        DB.session.add(user_obj)
        DB.session.commit()
        flask.flash('Welcome, {}! Please login.'.format(user_obj.username))
        flask_template = flask.redirect(flask.url_for('handle_login'))
    else:
        flask.flash('Hmmm, seems like something happened.')
        flask_template = flask.render_template("register.html", form=form)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


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


@app.route('/logs', methods=['GET'])
@flask_login.login_required
def logs():
    """
    This is to handle the requests of the application's logs.

    Returns:
        flask.template with all logs of the application.
    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.gmtime())))

    if flask_login.current_user.is_authenticated:
        int_id = user.get_user_id(flask.session['email'])

        str_page = _CONTAINER

        lst_data = common.get_logs()

        if lst_data:
            str_inner = """<div class="table-responsive">
                <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                <thead>
                    <tr>
                      <th>ID</th>
                      <th>Error Message</th>
                      <th>SQL executed</th>
                      <th>Date</th>
                      <th>Timestamp</th>
                    </tr>
                  </thead>
                """
            for row in lst_data:
                str_inner += "<tr>"
                for int_id, column in enumerate(row):
                    if int_id == 2:
                        str_inner += "<td><code>{}</code></td>".format(column)
                    else:
                        str_inner += "<td>{}</td>".format(column)
                str_inner += "</tr>"
            str_inner += """</table>
                      </div>"""
        else:
            str_inner = "<br><h1 align='center'>No logs registered.</h1>"

        template_return = flask.render_template('_blank.html',
                                                str_to_display=str_page.format(str_inner))
    else:
        utils.debug("Rendering '/login' page.")

        template_return = flask.redirect('/login')
        flask.session['next_url'] = flask.request.path

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

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


def generate_form(str_editing, lst_columns, lst_values):
    """
    Create a form with the columns and values passed as arguments so it can be rendered in a block
    content on a template.

    Args:
        str_editing: Type of table to edit.
        lst_columns: Columns of the table to be added into the form.
        lst_values: Values of the table to be added into the form.

    Returns:
        string with the form for the block content of the template.

    """
    str_inner_form = ""

    for column, value in zip(lst_columns, lst_values):
        str_disable = """ disabled""" if (column == 'ID') else " "

        if column == "StorageID":
            column = "Storage"
            lst_ncolumns = storage.get_storages()
            str_inner = ""
            for row in lst_ncolumns:
                str_inner += """<option value="{}">{}</option>\n""".format(row[0], row[1])

            str_inner_form += """<label for="str{column}">{column}</label>
            <select name="str{column}" class="form-control">
                {str_inner}
            </select>""".format(column=column, str_inner=str_inner)
        elif column == "CategoryID":
            column = "Category"
            lst_ncolumns = category.get_categories()
            str_inner = ""
            for row in lst_ncolumns:
                str_inner += """<option value="{}">{}</option>\n""".format(row[0], row[1])

            str_inner_form += """<label for="str{column}">{column}</label>
            <select name="str{column}" class="form-control">
                {str_inner}
            </select>""".format(column=column, str_inner=str_inner)
        else:
            str_inner_form += """<label for="str{column}">{column}</label>
        <input type="text" class="form-control" id="str{column}" name="str{column}" value="{value}" 
        placeholder="{value}" {disable}>""".format(column=column, value=value, disable=str_disable)

    str_form = """
    <div>
        <form action="#" method="post">
          <div class="form-group">
            {}
          </div>
          <div class="form-group row">
            <div class="col-sm-10">
              <button type="submit" class="btn btn-primary">Update {}</button>
            </div>
          </div>
        </form>
    </div>""".format(str_inner_form, str_editing.title())

    return _CONTAINER.format(str_form)

# with open(JSON_PATH) as f:
#     config = json.load(f)
