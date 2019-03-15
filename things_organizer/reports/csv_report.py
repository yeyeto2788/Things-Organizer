import os
import csv

from things_organizer import utils
from things_organizer.db import db_models


CSV_PATH = os.path.join(utils.REPORT_PATH, 'CSV')


class CSV:

    def __init__(self, file_name, int_user):
        """
        Constructor method for the CSV report generator.

        Args:
            file_name: Name for the `.csv` file.

        """
        self.file_name = '{}.csv'.format(file_name)
        self.user_id = int_user

        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)

    def get_all_things(self):
        """
        Make a representation of the database to `.csv` file with all things in database.

        """

        things = db_models.Thing.query.filter_by(user_id=self.user_id).all()
        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]

        things_refined = [row.__dict__ for row in things]
        for data in things_refined:
            data.pop('_sa_instance_state', None)

        self.write_file(column_names, things_refined)

    def get_by_category(self, int_id):
        """
        Make a representation of the database to `.csv` file with all things in database filtered
        by category.

        Args:
            int_id: ID of the category to filter by.

        """

        str_remove = 'category_id'
        category = db_models.Category.query.filter_by(id=int_id).first()
        things = db_models.Thing.query.filter_by(user_id=self.user_id, category=category).all()

        things_refined = [row.__dict__ for row in things]
        for data in things_refined:
            data.pop('_sa_instance_state', None)
            data.pop(str_remove, None)

        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
        column_names.remove(str_remove)
        self.write_file(column_names, things_refined)

    def get_by_storage(self, int_id):
        """
        Make a representation of the database to `.csv` file with all things in database filtered
        by storage.

        Args:
            int_id: ID of the storage to filter by.

        """

        str_remove = 'storage_id'
        storage = db_models.Storage.query.filter_by(id=int_id).first()
        things = db_models.Thing.query.filter_by(user_id=self.user_id, storage=storage).all()

        things_refined = [row.__dict__ for row in things]
        for data in things_refined:
            data.pop('_sa_instance_state', None)
            data.pop(str_remove, None)

        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
        column_names.remove(str_remove)
        self.write_file(column_names, things_refined)

    def write_file(self, lst_columns, things):
        """
        Common method for writing data into the `.csv` file.

        Args:
            lst_columns: Name of the columns of the file.
            things: Dictionary with the things to be stored.

        """
        file_dir = os.path.join(CSV_PATH, self.file_name)

        with open('{}'.format(file_dir), mode='w') as csv_file:
            file_writer = csv.DictWriter(csv_file, fieldnames=lst_columns)
            file_writer.writeheader()

            for row in things:
                file_writer.writerow(row)

        csv_file.close()
