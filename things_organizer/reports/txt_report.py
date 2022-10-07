"""

Report generator in `.txt` format in 3 different formats:

All items on database.
All items based on a category.
All items based on a storage.

Once report is generate it should return the directory of the file.

"""

import os

from prettytable import PrettyTable

import things_organizer.constants
from things_organizer.reports.base_report import BaseReport


class ReportTXT(BaseReport):
    """
    `.txt` generator class to be use when creating reports.

    Attributes:
        file_directory: Directory where report will be saved.
        file_name: Name to be used for the file.1
        user_id: User id to query all things from that id.

    Examples:
        ```
        from things_organizer.reports import TXT_Report

        txt_report = TXT_Report('all_things', 1)
        txt_report.get_all_things()

        # Change name of the file for not overwriting it.
        txt_report.file_name('all_by_category.txt', 2)
        txt_report.get_by_category()

        # Change name of the file for not overwriting it.
        txt_report.file_name('all_by_storage.txt', 2)
        txt_report.get_by_storage()

        ```

    """

    def __init__(self, file_name, int_user):
        """
        Constructor method for the ReportTXT report generator.

        Args:
            file_name: Name for the `.txt` file.

        """
        self.file_directory = os.path.join(
            things_organizer.constants.REPORT_PATH, "TXT"
        )
        self.file_name = f"{file_name}.txt"
        self.user_id = int_user

        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

    def generate_by_category(self, category_id):
        category_obj = self.get_category(category_id)
        column_names, things = self.get_things_by_category(category_id)

        self.write_file(
            column_names,
            things,
            f"All things sorted by '{category_obj.name}' Category",
        )

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def generate_by_storage(self, storage_id):
        storage_obj = self.get_storage(storage_id)
        column_names, things = self.get_things_by_category(storage_id)

        self.write_file(
            column_names,
            things,
            f"All things sorted by '{storage_obj.name}' Storage",
        )

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def generate_all(self):
        column_names, things = self.get_things()
        self.write_file(column_names, things, "All things on database")

        file_dir = os.path.join(self.file_directory, self.file_name)

        return os.path.realpath(file_dir)

    def write_file(self, lst_columns, things, str_title: str = None):
        """
        Common method for writing data into the `.txt` file.

        Args:
            lst_columns: Name of the columns of the file.
            things: Dictionary with the things to be stored.
            str_title: Title to be written on the `.txt` file.

        """

        file_dir = os.path.join(self.file_directory, self.file_name)

        if "user_id" in lst_columns:
            lst_columns.remove("user_id")

        table_data = PrettyTable(lst_columns)
        int_total = 0

        for row in things:
            data = row.__dict__
            data.pop("_sa_instance_state", None)
            data.pop("user_id", None)
            column_lst = []
            int_total += row.quantity

            for column_name in lst_columns:
                column_lst.append(data[column_name])
            table_data.add_row(column_lst)

        with open(file_dir, mode="w", encoding="utf-8") as txt_file:
            txt_file.write(f"\n\n{str_title}\n\n")
            file_data = table_data.get_string(title=str_title)
            txt_file.write(file_data)
            txt_file.write("\n\n")

            if things:
                total_data = PrettyTable(["Total Items"])
                total_data.add_row([int_total])
                txt_file.write(str(total_data))

        txt_file.close()
