from flask_wtf import FlaskForm
from wtforms import StringField

from things_organizer.web_app.storages.models import Storage


class StorageForm(FlaskForm):
    """
    FlaskForm for adding storage.

    """

    name = StringField(label='Storage Name')
    location = StringField(label='Location')

    def validate(self):
        """
        Validation of the Storage form checking whether the storage name
        and location pair already exists or not.

        Returns:
            True if the pair does not exists, else False.

        """

        bln_return = True

        if not FlaskForm.validate(self):
            bln_return = False

        if Storage.query.filter_by(
                name=self.name.data,
                location=self.location.data
        ).first():
            bln_return = False

        return bln_return
