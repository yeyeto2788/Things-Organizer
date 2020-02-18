from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError

from things_organizer.categories.models import Category


class CategoryForm(FlaskForm):
    """
    FlaskForm for adding a category.

    """

    name = StringField(label='Category Name')

    def validate_name(self, name_field):
        """
        Validate that the category name does not exists on the database.

        Args:
            name_field: Name of the category to be checked.

        Returns:
            True if name does not exists, else False.

        """
        if Category.query.filter_by(name=name_field.data).first():
            raise ValidationError('This category already exists.')