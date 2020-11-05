"""

Report generator in `.csv` format in 3 different formats:

All items on database.
All items based on a category.
All items based on a storage.

Once report is generate it should return the directory of the file.

"""

import csv
import os

from things_organizer import utils
from things_organizer.reports.base_report import BaseReport


class ReportCSV(BaseReport):
    """
    `.csv` generator class to be use when creating reports.

    Attributes:
        file_directory: Directory where report will be saved.
        file_name: Name to be used for the file.1
        user_id: User id to query all things from that id.

    Examples:
        ```
        from things_organizer.reports import CSV_Report

        csv_report = CSV_Report('all_things', 1)
        csv_report.get_all_things()

        # Change name of the file for not overwriting it.
        csv_report.file_name('all_by_category.csv', 2)
        csv_report.get_by_category()

        # Change name of the file for not overwriting it.
        csv_report.file_name('all_by_storage.csv', 2)
        csv_report.get_by_storage()

        ```

    """

    def __init__(self, file_name, int_user):
        """
        Constructor method for the ReportCSV report generator.

        Args:
            file_name: Name for the `.csv` file.

        """

        self.file_directory = os.path.join(utils.REPORT_PATH, 'CSV')
        self.file_name = '{}.csv'.format(file_name)
        self.user_id = int_user

        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

    def generate_by_category(self, category_id):
        column_names, things = self.get_things_by_category(category_id)
        lst_remove = ["category_id"]
        things_refined = self._remove_data([row.__dict__ for row in things],
                                           lst_remove)
        self.write_file(column_names, things_refined)

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def generate_by_storage(self, storage_id):
        column_names, things = self.get_things_by_category(storage_id)
        lst_remove = ["storage_id"]
        things_refined = self._remove_data([row.__dict__ for row in things],
                                           lst_remove)
        self.write_file(column_names, things_refined)

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def generate_all(self):
        column_names, things = self.get_things()
        lst_remove = ["user_id"]
        things_refined = self._remove_data([row.__dict__ for row in things],
                                           lst_remove)
        self.write_file(column_names, things_refined)
        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def write_file(self, lst_columns, things, str_title: str = None):
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
