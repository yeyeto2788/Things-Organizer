"""

Report generator in `.txt` format in 3 different formats:

All items on database.
All items based on a category.
All items based on a storage.

Once report is generate it should return the directory of the file.

"""

import os

from prettytable import PrettyTable

from things_organizer import utils
from things_organizer.db import db_models


class TXT:

    def __init__(self, file_name, int_user):
        """
        Constructor method for the TXT report generator.

        Args:
            file_name: Name for the `.txt` file.

        """
        self.file_directory = os.path.join(utils.REPORT_PATH, 'TXT')
        self.file_name = '{}.txt'.format(file_name)
        self.user_id = int_user

        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

    def get_all_things(self):
        """
        Make a representation of the database to `.txt` file with all things in database.

        Returns:
            Path of the file created.

        """

        things = db_models.Thing.query.filter_by(user_id=self.user_id).all()
        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
        self.write_file(column_names, things, 'All things on database')

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def get_by_category(self, int_id):
        """
        Make a representation of the database to `.txt` file with all things in database filtered
        by category.

        Args:
            int_id: ID of the category to filter by.

        Returns:
            Path of the file created.

        """
        category = db_models.Category.query.filter_by(id=int_id).first()

        things = db_models.Thing.query.filter_by(user_id=self.user_id, category=category).all()
        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
        column_names.remove('category_id')
        self.write_file(column_names, things,
                        'All things sorted by \'{}\' Category'.format(category.name))

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def get_by_storage(self, int_id):
        """
        Make a representation of the database to `.txt` file with all things in database filtered
        by storage.

        Args:
            int_id: ID of the storage to filter by.

        Returns:
            Path of the file created.

        """

        storage = db_models.Storage.query.filter_by(id=int_id).first()

        things = db_models.Thing.query.filter_by(user_id=self.user_id, storage=storage).all()
        column_names = [str(name).split('.')[1] for name in db_models.Thing.__table__.columns]
        column_names.remove('storage_id')
        self.write_file(column_names, things,
                        'All things sorted by \'{}\' Storage'.format(storage.name))

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def write_file(self, lst_columns, things, str_title):
        """
        Common method for writing data into the `.txt` file.

        Args:
            lst_columns: Name of the columns of the file.
            things: Dictionary with the things to be stored.
            str_title: Title to be written on the `.txt` file.

        """

        file_dir = os.path.join(self.file_directory, self.file_name)

        if 'user_id' in lst_columns:
            lst_columns.remove('user_id')

        table_data = PrettyTable(lst_columns)
        int_total = 0

        for row in things:
            data = row.__dict__
            data.pop('_sa_instance_state', None)
            data.pop('user_id', None)
            column_lst = []
            int_total += row.quantity
            for column_name in lst_columns:
                column_lst.append(data[column_name])
            table_data.add_row(column_lst)

        with open('{}'.format(file_dir), mode='w') as txt_file:
            txt_file.write('\n\n{}\n\n'.format(str_title))
            file_data = table_data.get_string(title=str_title)
            txt_file.write(file_data)
            txt_file.write('\n\n')
            if things:
                total_data = PrettyTable(['Total Items'])
                total_data.add_row([int_total])
                txt_file.write(str(total_data))

        txt_file.close()
        print(int_total)
