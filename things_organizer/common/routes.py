import inspect
import time

import flask
import flask_login
from flask_restful import Resource
from sqlalchemy import or_

from things_organizer import utils
from things_organizer.categories.models import Category
from things_organizer.common.forms import LoginForm, SignupForm
from things_organizer.common.models import User
from things_organizer.extensions import database
from things_organizer.labels import QRLabel
from things_organizer.storages.models import Storage
from things_organizer.things.models import Thing


class HomeResource(Resource):
    @flask_login.login_required
    def get(self):
        """Main site where user goes to see available tools on the server
        and the description of them.

        Returns:
            Template of the different tools hosted.

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        utils.debug("Rendering 'Index' page.")

        template_return = flask.render_template('index.html')

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        return flask.Response(template_return, mimetype='text/html')


class LoginResource(Resource):
    def get(self):
        """Handles the login page based on the request method, if request is
        POST it will check user existence on the database. If the request is
        GET it will just send the login page.

        Returns:
            Flask template based on the request method.

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        form = LoginForm()
        flask_template = flask.render_template("login.html", form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        return flask.Response(flask_template, mimetype='text/html')

    def post(self):
        """

        Returns:

        """
        form = LoginForm()

        if form.validate_on_submit():
            user_obj = User.get_by_username(form.username.data)

            if user_obj is not None and user_obj.check_password(form.password.data):
                flask_login.login_user(user_obj, form.remember_me.data)
                flask.flash("Welcome, {}!.".format(user_obj.username))

                flask_template = flask.render_template('index.html', username=user_obj.username)

            else:
                flask.flash('ERROR:Incorrect username or password.')
                flask_template = flask.render_template("login.html", form=form)

        else:
            flask_template = flask.render_template("login.html", form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        return flask.Response(flask_template, mimetype='text/html')


class RegisterResource(Resource):
    def get(self):
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
        flask_template = flask.render_template("register.html", form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        return flask.Response(flask_template, mimetype='text/html')

    def post(self):

        form = SignupForm()

        if form.validate_on_submit():
            user_obj = User(email=form.email.data, username=form.username.data, password=form.password.data, )
            database.session.add(user_obj)
            database.session.commit()
            flask.flash('Welcome, {}! Please login.'.format(user_obj.username))
            flask_template = flask.redirect(flask.url_for('handle_login'))
            return flask_template

        else:
            flask.flash('ERROR: Hhmm, seems like there was an error registering you account.')
            flask_template = flask.render_template("register.html", form=form)

            utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                      time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            return flask.Response(flask_template, mimetype='text/html')


class SearchResource(Resource):
    @flask_login.login_required
    def get(self):
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
                things = Thing.query.filter(
                    User.id == flask_login.current_user.id, or_(
                        Thing.name.contains('{}%'.format(search_txt)),
                        Thing.description.contains('{}%'.format(search_txt)))
                ).all()

                if things:
                    template_text += 'Found <b>{}</b> items.\n\n'.format(len(things))

                    for int_index, thing in enumerate(things):
                        int_index += 1
                        template_text += '<b>Item {:02}</b>\n'.format(int_index)
                        template_text += '<b>Name:</b> {}\n'.format(str(thing.name))
                        template_text += '<b>Description:</b> {}\n'.format(str(thing.description))
                        storage = Storage.query.filter_by(id=thing.storage_id).first()
                        template_text += '<b>Storage:</b> {}\n'.format(storage.name)
                        template_text += '<b>Location:</b> {}\n'.format(storage.location)
                        category = Category.query.filter_by(id=thing.category_id).first()
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
        return flask.Response(flask_template, mimetype='text/html')


class AboutResource(Resource):
    def get(self):
        """
        Shows information about the project.

        Returns:
            Template of the different tools hosted.

        """

        template_return = flask.render_template('about.html')

        return flask.Response(template_return, mimetype='text/html')


class LabelResource(Resource):
    @flask_login.login_required
    def get(self, int_id):
        """
        Generate the label for a given item.

        Args:
            int_id: ID of the item

        Returns:
            Flask template based on the request method.

        """

        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        thing = Thing.query.filter_by(user_id=flask_login.current_user.id, id=int_id).first()

        storage = Storage.query.filter_by(id=thing.storage_id).first()

        if thing:
            label = QRLabel(thing.name, thing.description, storage.name, storage.location)
            label.generate_label()

            template_return = flask.send_from_directory(
                label.file_directory, label.file_name, as_attachment=True)
            flask.flash("Label '{}' generated.".format(label.file_name))

            return template_return

        else:
            template_return = flask.redirect(flask.url_for('handle_things'))
            utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                      time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

            return flask.Response(template_return, mimetype='text/html')


class LogoutResource(Resource):
    def get(self):
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
