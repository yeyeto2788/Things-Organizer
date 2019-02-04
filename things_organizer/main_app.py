"""
Main logic of the application is declared here.

"""
import time
import base64
import inspect

import flask
import flask_restful

from things_organizer.data_management import category, common, user, storage, tag, things
from things_organizer import utils
from things_organizer.api import categories

app = flask.Flask(__name__, static_url_path="/static")


API = flask_restful.Api(app)

API.add_resource(categories.CategoriesAPI, '/api/categories', '/api/categories/<int:int_id>')

_CONTAINER = """
 <div id="content-wrapper">
    <div class="container-fluid">
    {}
    </div>
</div>
"""


@app.route('/')
@app.route('/home')
def root():
    """
    Main site where user goes to see available tools on the server and the description of them.

    Returns:
        Template of the different tools of hosted.

    """
    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    utils.debug("Rendering 'Index' page.")

    template_return = flask.render_template('index.html')

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return template_return


@app.route('/edit/<string:str_to_edit>/<int:int_id>', methods=['POST', 'GET'])
def handle_edit(str_to_edit, int_id):
    """
    Edit records depending of the type of table is being requested.

    Args:
        str_to_edit:
        int_id:

    Returns:
        Flask template based on the request method.

    """

    lst_to_edit = {'category': common.TBL_CATEGORIES,
                   'storage': common.TBL_STORAGE,
                   'thing': common.TBL_THINGS,
                   'tag': common.TBL_TAGS}

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    template_return = flask.render_template('404.html'), 404

    if (str_to_edit in lst_to_edit.keys()) and 'email' in flask.session:

        lst_pre_values = common.get_data_by_id(lst_to_edit[str_to_edit], int_id)
        lst_columns = common.get_columns_from(lst_to_edit[str_to_edit])

        if flask.request.method == 'GET':

            str_return = generate_form(str_to_edit, lst_columns, lst_pre_values)
            utils.debug("Redirecting to the edit page for {}.".format(str_to_edit))
            template_return = flask.render_template('_blank.html', str_to_display=str_return)

        else:
            form_data = flask.request.form
            data_keys = []
            lst_new_values = []

            for data_key in form_data.keys():
                data_keys.append(data_key)
                lst_new_values.append(form_data[data_key])

            # Add the ID from requests since it is not enable on the form
            # lst_new_values.insert(0, int_id)

            utils.debug('lst_columns: ', lst_columns, 'lst_new_values', lst_new_values)

            bln_return = common.update_table_row(lst_to_edit[str_to_edit],
                                                 lst_columns, lst_new_values, int_id)
            if bln_return:
                if str_to_edit == "category":
                    utils.debug("Redirecting to '{}' page.".format(str_to_edit))
                    template_return = flask.redirect(flask.url_for("handle_categories"))
                elif str_to_edit == "storage":
                    utils.debug("Redirecting to '{}' page.".format(str_to_edit))
                    template_return = flask.redirect(flask.url_for("handle_storage"))
                elif str_to_edit == "thing":
                    utils.debug("Redirecting to '{}' page.".format(str_to_edit))
                    template_return = flask.redirect(flask.url_for("handle_things"))
                elif str_to_edit == "tag":
                    utils.debug("Redirecting to '{}' page.".format(str_to_edit))
                    template_return = flask.redirect(flask.url_for("handle_tags"))

    elif 'email' not in flask.session:
        utils.debug("Redirecting to 'Login' page.")
        template_return = flask.redirect('/login')
    else:
        utils.debug("Redirecting to '404' page.")
        template_return = flask.redirect(flask.url_for('page_not_found'))

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
    if flask.request.method == 'GET':
        flask_template = flask.render_template('login.html')
    else:
        str_email = flask.request.form['inputEmail']
        str_password = flask.request.form['inputPassword']

        if user.is_user(str_email, base64.b64encode(str_password.encode('ascii')).decode("utf-8")):
            flask.session['email'] = str_email
            int_id = user.get_user_id(str_email)
            user.add_session(int_id)

            if 'next_url' in flask.session:
                flask_template = flask.redirect(flask.session['next_url'])
                utils.debug("Redirecting to '{}' page.".format(flask.session['next_url']))
            else:
                flask_template = flask.redirect(flask.url_for('root'))
                utils.debug("Redirecting to 'root' page.")
        else:
            str_page = """<h1 align="center">Not possible to sign in :(</h1>"""
            utils.debug("Redirecting to '_blank' page due to problems logging in.")
            flask_template = flask.render_template('_blank.html',
                                                   str_to_display=_CONTAINER.format(str_page))

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
    # remove the username from the session if it's there
    if 'email' in flask.session:
        int_id = user.get_user_id(flask.session['email'])
        flask.session.pop('email', None)
        user.delete_session(int_id)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return flask.redirect(flask.url_for('root'))


@app.route('/categories', methods=['POST', 'GET'])
def handle_categories():
    """
    Handles the categories creation and rendering on the page.

    Returns:
        Flask template based on the request method.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    html_data = {
        "form_url": flask.url_for("handle_categories"),
        "form_items": ["Category Name"],
        "table_columns": ["ID", "Name"],
        "table_name": common.TBL_CATEGORIES,
        "edit_url": "category"
    }

    if 'email' in flask.session:
        int_id = user.get_user_id(flask.session['email'])

        if flask.request.method == 'GET':

            if common.is_table_configured(common.TBL_CATEGORIES):
                    lst_tdata = category.get_categories()
            else:
                lst_tdata = None

            template_return = flask.render_template('_table.html', table_data=lst_tdata,
                                                    html_data=html_data)
        else:
            str_category = flask.request.form['strCategoryName']

            if user.check_session(int_id):

                if category.add_category(str_category):
                    lst_tdata = category.get_categories()

                else:
                    lst_tdata = None

                template_return = flask.render_template('_table.html', table_data=lst_tdata,
                                                        html_data=html_data)
            else:
                template_return = flask.redirect(flask.url_for('page_not_found'))

    else:
        template_return = flask.redirect('/login')
        flask.session['next_url'] = flask.request.path

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return template_return


@app.route('/storages', methods=['POST', 'GET'])
def handle_storage():
    """
    Handles the storage creation and rendering on the page.

    Returns:
        Flask template based on the request method.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    html_data = {
        "form_url": flask.url_for("handle_storage"),
        "form_items": ["Storage name", "Storage location"],
        "table_columns": ["ID", "Name", "Location"],
        "table_name": common.TBL_STORAGE,
        "edit_url": "storage"
    }

    if 'email' in flask.session:
        int_id = user.get_user_id(flask.session['email'])

        if flask.request.method == 'GET':

            if common.is_table_configured(common.TBL_STORAGE):
                    lst_tdata = storage.get_storages()
            else:
                lst_tdata = None

            template_return = flask.render_template('_table.html', table_data=lst_tdata,
                                                    html_data=html_data)
        else:
            str_storage = flask.request.form['strStoragename']
            str_location = flask.request.form['strStoragelocation']

            if user.check_session(int_id):

                if storage.add_storage(str_storage, str_location):
                    lst_tdata = storage.get_storages()

                else:
                    lst_tdata = None

                template_return = flask.render_template('_table.html', table_data=lst_tdata,
                                                        html_data=html_data)
            else:
                template_return = flask.redirect(flask.url_for('page_not_found'))

    else:
        template_return = flask.redirect('/login')
        flask.session['next_url'] = flask.request.path

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

    if flask.request.method == 'GET':
        flask_template = flask.render_template('register.html', )

    else:
        str_name = flask.request.form['firstName']
        str_lastname = flask.request.form['lastName']
        str_email = flask.request.form['inputEmail']
        str_password = flask.request.form['inputPassword']
        str_pswd_confirmation = flask.request.form['confirmPassword']

        encoded = base64.b64encode(str_password.encode('ascii')).decode("utf-8")

        str_page = """ 
        <div>
        <p class="lead" align="center">Seems like the email <code>{}</code> is
         already in our system.<br>You can <a href="javascript:history.back()">
         go back</a> to the previous page, or 
        <a href="/home">return home</a>.</p>
        </div>""".format(str_email)

        if str_password == str_pswd_confirmation:

            if user.register_user(str_name, str_lastname, str_email, encoded):
                flask.session['email'] = str_email
                user.add_session(
                    user.get_user_id(str_email))
                str_page = """<h1 align="center">Register successful!</h1>
                <br>
                <h3 align="center">
                  Please go to <a href='/home'>Home</a> to start organizing things!
                </h3>"""
        else:
            str_page = """<div>
                            <p class="lead" align="center">Please verify your password.<br>
                             <a href="javascript:history.back()">
                             Go back</a> to the previous page.</p>
                            </div>
                            """

        flask_template = flask.render_template('_blank.html',
                                               str_to_display=_CONTAINER.format(str_page))

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


@app.route("/tags", methods=['POST', 'GET'])
@app.route("/tags.html", methods=['POST', 'GET'])
def handle_tags():
    """
        Handles the showing or not of the tags on the system.

        Returns:
            flask template.

        """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    html_data = {
        "form_url": flask.url_for("handle_tags"),
        "form_items": ["Tag title"],
        "table_columns": ["ID", "Title"],
        "table_name": common.TBL_TAGS,
        "edit_url": "tag"
    }

    if 'email' in flask.session:
        int_id = user.get_user_id(flask.session['email'])

        if flask.request.method == 'GET':

            if common.is_table_configured(common.TBL_TAGS):
                    lst_tdata = tag.get_tags()
            else:
                lst_tdata = None

            template_return = flask.render_template('_table.html', table_data=lst_tdata,
                                                    html_data=html_data)
        else:
            str_title = flask.request.form['strTitle']

            if user.check_session(int_id):

                if tag.add_tag(str_title):
                    lst_tdata = tag.get_tags()

                else:
                    lst_tdata = None

                template_return = flask.render_template('_table.html', table_data=lst_tdata,
                                                        html_data=html_data)
            else:
                template_return = flask.redirect(flask.url_for('page_not_found'))

    else:
        template_return = flask.redirect('/login')
        flask.session['next_url'] = flask.request.path

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return template_return


@app.route("/things", methods=['GET'])
@app.route("/things.html", methods=['GET'])
def handle_things():
    """
    Handles the showing or not of the things belonging to the user.

    Returns:
        flask template.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    if 'email' in flask.session:
        int_id = user.get_user_id(flask.session['email'])

        if user.check_session(int_id):
            lst_tdata = things.get_user_things(int_id)

            if not lst_tdata:
                lst_tdata = None

            utils.debug("Redirecting to 'things' page.")
            flask_template = flask.render_template('things.html', table_data=lst_tdata)

        else:
            utils.debug("Redirecting to 'login' page.")
            flask_template = flask.redirect(flask.url_for('handle_login'))
            flask.session['next_url'] = flask.request.path
    else:
        utils.debug("Redirecting to 'login' page.")
        flask_template = flask.redirect(flask.url_for('handle_login'))
        flask.session['next_url'] = flask.request.path

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    return flask_template


@app.route('/logs', methods=['GET'])
def logs():
    """
    This is to handle the requests of the application's logs.

    Returns:
        flask.template with all logs of the application.
    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.gmtime())))

    if 'email' in flask.session:
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
