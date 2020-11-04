from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email

from things_organizer.web_app.users.models import User


class LoginForm(FlaskForm):
    """
    FlaskForm for login purposes.

    """

    username = StringField(
        label='Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired()]
    )
    remember_me = BooleanField(
        label='Keep me logged in'
    )


class SignupForm(FlaskForm):
    """
    FlaskForm for registering/signup purposes.

    """

    username = StringField(
        label='Username',
        validators=[
            DataRequired(),
            Length(3, 80),
            Regexp(
                '^[A-Za-z0-9_]{3,}$',
                message='Username should consist of numbers, '
                        'letters, and underscores.'
            )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Passwords must match.')
        ]
    )
    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 120),
            Email()
        ]
    )

    def validate_email(self, email_field):
        """
        Check whether the user's email exists on the database.

        Args:
            email_field: email to be checked.

        Returns:
            True if not found, else False.

        """

        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError(
                'There already is a user with this email address.')

    def validate_username(self, username_field):
        """
        Check whether the username exists on the database.

        Args:
            username_field: username to be checked.

        Returns:
            True if not found, else False.

        """

        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
