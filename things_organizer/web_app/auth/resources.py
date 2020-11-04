import inspect
import time

import flask
import flask_login
from flask_restful import Resource

from things_organizer import utils
from things_organizer.web_app.auth.forms import LoginForm, SignupForm
from things_organizer.web_app.users.models import User
from things_organizer.extensions import database


class LoginResource(Resource):
    def get(self):
        """Handles the login page based on the request method, if request is
        POST it will check user existence on the database. If the request is
        GET it will just send the login page.

        Returns:
            Flask template based on the request method.

        """
        utils.debug(
            "** {} - INI\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )

        form = LoginForm()
        flask_template = flask.render_template("login.html", form=form)

        utils.debug(
            "** {} - END\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )
        return flask.Response(flask_template, mimetype='text/html')

    def post(self):
        """

        Returns:

        """
        form = LoginForm()

        if form.validate_on_submit():
            user_obj = User.get_by_username(form.username.data)

            if user_obj is not None and user_obj.check_password(
                    form.password.data):
                flask_login.login_user(user_obj, form.remember_me.data)
                flask.flash("Welcome, {}!.".format(user_obj.username))

                if flask.request.values.get('next'):
                    return flask.redirect(flask.request.values.get('next'))

                else:
                    flask_template = flask.render_template(
                        'index.html',
                        username=user_obj.username
                    )

            else:
                flask.flash('ERROR:Incorrect username or password.')
                flask_template = flask.render_template("login.html", form=form)

        else:
            flask_template = flask.render_template("login.html", form=form)

        utils.debug(
            "** {} - END\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )

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

        utils.debug(
            "** {} - INI\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )

        form = SignupForm()
        flask_template = flask.render_template("register.html", form=form)

        utils.debug(
            "** {} - END\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )

        return flask.Response(flask_template, mimetype='text/html')

    def post(self):
        """

        Returns:

        """
        form = SignupForm()

        if form.validate_on_submit():
            user_obj = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
            )
            database.session.add(user_obj)
            database.session.commit()
            flask.flash('Welcome, {}! Please login.'.format(user_obj.username))
            flask_template = flask.redirect(flask.url_for('handle_login'))
            return flask_template

        else:
            flask.flash(
                'ERROR: Hhmm, seems like there was an '
                'error registering you account.'
            )
            flask_template = flask.render_template("register.html", form=form)

            utils.debug(
                "** {} - END\t{} **\n".format(
                    inspect.stack()[0][3],
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.gmtime())
                )
            )

            return flask.Response(flask_template, mimetype='text/html')


class LogoutResource(Resource):

    def get(self):
        """
        Remove the user's flask session.

        Returns:
            It will redirect the user to home.

        """

        utils.debug(
            "** {} - INI\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )
        # Remove the username from the session if it's there
        flask_login.logout_user()

        utils.debug(
            "** {} - END\t{} **\n".format(
                inspect.stack()[0][3],
                time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime())
            )
        )

        return flask.redirect(flask.url_for('handle_root'))
