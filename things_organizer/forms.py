from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
# from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, url, ValidationError

from things_organizer.db.db_models import User, Category, Storage, Tag, Thing


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Keep me logged in')


class SignupForm(FlaskForm):
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


class ThingForm(FlaskForm):
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


class CategoryForm(FlaskForm):
    name = StringField(label='Category Name')

    def validate_name(self, name_field):
        if Category.query.filter_by(name=name_field.data).first():
            raise ValidationError('This category already exists.')


class StorageForm(FlaskForm):
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
    name = StringField(label='Tag Name')
