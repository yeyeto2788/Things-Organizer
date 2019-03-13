import os
import csv

from things_organizer import utils
from things_organizer.db import db_models


CSV_PATH = os.path.join(utils.REPORT_PATH, 'CSV')


class CSV:

    def __init__(self, file_name):
        """
        Constructor method for the CSV report generator.

        Args:
            file_name: Name for the `.csv` file.

        """
        self.file_name = '{}.csv'.format(file_name)
        self.file_dir = os.path.join(CSV_PATH, self.file_name)

        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)

    def get_all_things(self):
        """
        Make a representation of the database to `.csv` file with all things in database.

        """

        things = db_models.Thing.query.all()
        with open('{}'.format(self.file_dir), mode='w') as csv_file:
            table_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
            print(table_names)
            file_writer = csv.DictWriter(csv_file, fieldnames=table_names)
            file_writer.writeheader()

            for row in things:
                data = row.__dict__
                data.pop('_sa_instance_state', None)
                file_writer.writerow(data)

    def get_by_category(self, int_id):
        """
        Make a representation of the database to `.csv` file with all things in database filtered
        by category.

        Args:
            int_id: ID of the category to filter by.

        """
        category = db_models.Category.query.filter_by(id=int_id).first()

        things = db_models.Thing.query.filter_by(category=category).all()
        with open('{}'.format(self.file_dir), mode='w') as csv_file:
            table_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
            print(table_names)
            file_writer = csv.DictWriter(csv_file, fieldnames=table_names)
            file_writer.writeheader()

            for row in things:
                data = row.__dict__
                data.pop('_sa_instance_state', None)
                file_writer.writerow(data)

    def get_by_storage(self, int_id):
        """
        Make a representation of the database to `.csv` file with all things in database filtered
        by storage.

        Args:
            int_id: ID of the storage to filter by.

        """

        storage = db_models.Storage.query.filter_by(id=int_id).first()

        things = db_models.Thing.query.filter_by(storage=storage).all()
        with open('{}'.format(self.file_dir), mode='w') as csv_file:
            table_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
            print(table_names)
            file_writer = csv.DictWriter(csv_file, fieldnames=table_names)
            file_writer.writeheader()

            for row in things:
                data = row.__dict__
                data.pop('_sa_instance_state', None)
                file_writer.writerow(data)
