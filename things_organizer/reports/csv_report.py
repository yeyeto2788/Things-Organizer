"""

Report generator in `.csv` format in 3 different formats:

All items on database.
All items based on a category.
All items based on a storage.

Once report is generate it should return the directory of the file.

"""

import os
import csv

from things_organizer import utils
from things_organizer.db import db_models


class CSV:

    def __init__(self, file_name, int_user):
        """
        Constructor method for the CSV report generator.

        Args:
            file_name: Name for the `.csv` file.

        """

        self.file_directory = os.path.join(utils.REPORT_PATH, 'CSV')
        self.file_name = '{}.csv'.format(file_name)
        self.user_id = int_user

        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

    def get_all_things(self):
        """
        Make a representation of the database to `.csv` file with all things in database.

        Returns:
            Path of the file created.

        """

        things = db_models.Thing.query.filter_by(user_id=self.user_id).all()
        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]

        things_refined = self._remove_data([row.__dict__ for row in things])

        self.write_file(column_names, things_refined)

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def get_by_category(self, int_id):
        """
        Make a representation of the database to `.csv` file with all things in database filtered
        by category.

        Args:
            int_id: ID of the category to filter by.

        Returns:
            Path of the file created.

        """

        lst_remove = ['category_id']
        category = db_models.Category.query.filter_by(id=int_id).first()
        things = db_models.Thing.query.filter_by(user_id=self.user_id, category=category).all()

        things_refined = self._remove_data([row.__dict__ for row in things], lst_remove)

        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]

        for str_remove in lst_remove:
            column_names.remove(str_remove)

        self.write_file(column_names, things_refined)

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def get_by_storage(self, int_id):
        """
        Make a representation of the database to `.csv` file with all things in database filtered
        by storage.

        Args:
            int_id: ID of the storage to filter by.

        Returns:
            Path of the file created.

        """

        lst_remove = ['storage_id']
        storage = db_models.Storage.query.filter_by(id=int_id).first()
        things = db_models.Thing.query.filter_by(user_id=self.user_id, storage=storage).all()

        things_refined = self._remove_data([row.__dict__ for row in things], lst_remove)

        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]

        for str_remove in lst_remove:
            column_names.remove(str_remove)
        self.write_file(column_names, things_refined)

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    @staticmethod
    def _remove_data(things, lst_remove=None):
        """
        Static method to remove not needed items from the report.

        Args:
            things: Thing items on which removal will be applied.
            lst_remove: Items to be removed.

        Returns:
            Modified things parameter.

        """

        for data in things:
            data.pop('_sa_instance_state', None)
            data.pop('user_id', None)

            if lst_remove is not None:
                for str_remove in lst_remove:
                    if str_remove in data:
                        data.pop(str_remove, None)

        return things

    def write_file(self, lst_columns, things):
        """
        Common method for writing data into the `.csv` file.

        Args:
            lst_columns: Name of the columns of the file.
            things: Dictionary with the things to be stored.

        """
        file_dir = os.path.join(self.file_directory, self.file_name)

        if 'user_id' in lst_columns:
            lst_columns.remove('user_id')

        with open('{}'.format(file_dir), mode='w') as csv_file:
            file_writer = csv.DictWriter(csv_file, fieldnames=lst_columns)
            file_writer.writeheader()

            for row in things:
                file_writer.writerow(row)

        csv_file.close()
