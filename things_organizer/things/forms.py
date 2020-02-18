from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import Regexp


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
        """
        Validation of the Things form checking for tags separated by comma.

        Returns:
            True if the form is validated by it parent, else False.
        """

        if not FlaskForm.validate(self):
            return False

        # Filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True