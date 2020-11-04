from flask_wtf import FlaskForm
from wtforms import StringField


class TagForm(FlaskForm):
    """
    FlaskForm for adding tags.

    """

    name = StringField(label='Tag Name')