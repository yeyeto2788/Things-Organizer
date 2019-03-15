"""
Form definitions for rendering on the HTML pages and make easier the load and set of
items on the page.

"""

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from things_organizer.db.db_models import User, Category, Storage, Tag, Thing


class CategoryForm(FlaskForm):
    """
    FlaskForm for adding a category.

    """

    name = StringField(label='Category Name')

    def validate_name(self, name_field):
        if Category.query.filter_by(name=name_field.data).first():
            raise ValidationError('This category already exists.')


class LoginForm(FlaskForm):
    """
    FlaskForm for login purposes.

    """

    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Keep me logged in')


class ReportForm(FlaskForm):
    """
    FlaskForm for selecting the report to be printed.

    """

    report_type = SelectField(label="Select type of file", coerce=int)
    data_type = SelectField(label="Select data for report", coerce=int)
    category = SelectField(label="Select Category", coerce=int)
    storage = SelectField(label="Select Storage", coerce=int)


class SignupForm(FlaskForm):
    """
    FlaskForm for registering/signup purposes.

    """

    username = StringField(
        label='Username',
        validators=[DataRequired(),
        Length(3, 80),
        Regexp('^[A-Za-z0-9_]{3,}$',
               message='Username should consist of numbers, letters, and underscores.')])
    password = PasswordField(
        'Password',
        validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class StorageForm(FlaskForm):
    """
    FlaskForm for adding storage.

    """

    name = StringField(label='Storage Name')
    location = StringField(label='Location')

    def validate(self):

        bln_return = True

        if not FlaskForm.validate(self):
            bln_return = False

        if Storage.query.filter_by(name=self.name.data, location=self.location.data).first():
            bln_return = False

        return bln_return


class TagForm(FlaskForm):
    """
    FlaskForm for adding tags.

    """

    name = StringField(label='Tag Name')


class ThingForm(FlaskForm):
    """
    FlaskForm for adding things.

    """

    name = StringField('Name')
    description = StringField('Description (Optional)')
    category = SelectField(label="Select a category", coerce=int)
    storage = SelectField(label="Select a storage", coerce=int)
    quantity = IntegerField(label="Please type how many items")
    unit = StringField('Unit for the item')
    tags = StringField(
        'Tags',
        validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                           message="Tags can only contain letters and numbers")])

    def validate(self):

        if not FlaskForm.validate(self):
            return False

        # Filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True

