"""

Main database operations are done at this level.


"""

import os
import sqlite3
from time import gmtime, strftime, time

from things_organizer import utils
from things_organizer.db import Errors

DB_PATH = os.path.normpath(os.path.join(os.path.dirname(utils.__file__), "data"))


class DataBase:
    """
    Database object to do all possible operation on DB.

    Attributes:
        close_connection: whether to close or not after each operation.
        str_db_name: Name of the database.
        db_connection: Connection from `sqlite3.connect`

    """
    close_connection = 1

    def __init__(self, str_db_name='things_organizer.db'):
        self.str_db_name = str_db_name
        self.db_connection = None
        self.close_connection = 0

    def close_db_connection(self):
        """
        Close connection if present, otherwise an error will be raised.

        Returns:
            True if connection closed, else False.
        """

        self.close_connection = 1

        bln_return = False

        try:
            if self.db_connection is not None:
                self.db_connection.close()
                bln_return = True
            else:
                raise Errors.DataBaseConnectionError("There is no active database connection.")

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.DataBaseError(excerror)

        return bln_return

    def connect_to_db(self, bln_create_db=0):
        """
        Connect to the database, by default if no name was given at the moment of the
        instance creation it will automatically connect to 'things_organizer.db'.

        Returns:
            True if connection OK, else False
        """

        bln_return = True

        str_dbdirectory = os.path.join(DB_PATH, self.str_db_name)
        if os.path.exists(str_dbdirectory) or bln_create_db:
            self.db_connection = sqlite3.connect(str_dbdirectory)
        else:
            raise Errors.DataBaseExistenceError(self.str_db_name)

        return bln_return

    def create_table(self, str_tname, lst_columns):
        """
        Create a table from the create_table_sql statement.

        Args:
            str_tname: Table name to be created.
            lst_columns: Columns to be added.

        Returns:
            True if table created, else False.
        """

        try:
            cursor = self.db_connection.cursor()
            str_columns = utils.convert_list_to_columns(lst_columns)
            cursor.execute("CREATE TABLE IF NOT EXISTS {} ({});".format(str_tname, str_columns))

            self.db_connection.commit()

            if self.close_connection:
                self.db_connection.close()

            return True

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.DataBaseError(excerror)

    def drop_table(self, str_tname):
        """
        Deletes a given table from the database.

        Args:
            str_tname: Table name.

        Returns:
            True if table was dropped, else `None`
        """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS {};".format(str_tname))

            self.db_connection.commit()

            if self.close_connection:
                self.db_connection.close()

            return True

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.DataBaseError(excerror)

    def execute_sql(self, str_command):
        """
        Executes any kind of query on the database.

        Args:
            str_command: Command to be executed.

        Returns:
            `None` if an error occurs on execution, else True
        """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(str_command)

            if not str_command.startswith("SELECT"):
                self.db_connection.commit()

            if self.close_connection:
                self.db_connection.close()

            return True

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.DataBaseError(excerror)
        except sqlite3.IntegrityError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.AlreadyExistsError(excerror)

    def get_db_tables(self):
        """
        Get all tables on the database.

        Returns:
            List with the name of the table, if error is raised on execution a `None` will be
            returned.
        """

        str_sql = "SELECT name FROM sqlite_master WHERE type='table';"

        try:
            lst_tables = []
            cursor = self.db_connection.cursor()

            for row in cursor.execute(str_sql):
                lst_tables.append([column for column in row])

            if self.close_connection:
                self.db_connection.close()

            return lst_tables

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.NotFoundError(excerror)

    def get_columns_names(self, str_tname):
        """
        Get the table column's names of a given table by the return of the `cursor.description`.

        Args:
            str_tname: Name of the table.

        Returns:
            List with the columns names. otherwise `None` will be returned.
        """

        str_sql = "SELECT * FROM {};".format(str_tname)

        try:

            cursor = self.db_connection.cursor()
            cursor.execute(str_sql)

            lst_tables = [str_cName[0] for str_cName in cursor.description]

            if self.close_connection:
                self.db_connection.close()

            return lst_tables

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.DataBaseError(excerror)

    def get_table_content(self, str_tname):
        """
        Perform a `SELECT * FROM <str_tname>` and return its result.

        Args:
            str_tname: Name of table to retrieve data from.

        Returns:
            List with table data if the table exists on `db` directory.
        """

        lst_tables = []
        str_sql = "SELECT * FROM {};".format(str_tname)

        try:

            cursor = self.db_connection.cursor()
            cursor.execute(str_sql)

            rows = cursor.fetchall()

            for row in rows:
                lst_tables.append([column for column in row])

            if self.close_connection:
                self.db_connection.close()

            return lst_tables

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            raise Errors.DataBaseError(excerror)

    def insert_into_table(self, str_tname, lst_values):
        """
        Insert values into a given table.

        Args:
            str_tname: Table name where data will be inserted.
            lst_values: values to be inserted.

        Returns:
            Integer of the row inserted, otherwise a `None` will be returned.
        """

        try:
            cursor = self.db_connection.cursor()

            str_values = utils.convert_list_to_values(lst_values)

            str_sql = "INSERT INTO {} VALUES({}) ;".format(str_tname, str_values)

            cursor.execute(str_sql)

            int_row_id = cursor.lastrowid
            self.db_connection.commit()

            if self.close_connection:
                self.db_connection.close()

            return int_row_id

        except sqlite3.OperationalError as excerror:
            utils.debug(excerror.__str__)
            return None


class DataBaseLogger(DataBase):
    """
    Database object to log all failures of the application.

    Attributes:
        tbl_name: Table name.
        tbl_columns: Name for the columns used in the table.
        db_name: Name for specific loggin db.
        db_log: instance of the Database.

    """

    tbl_name = 'Logs'
    tbl_columns = ['Message', 'strSQL', 'Date', 'Timestamp']
    db_name = 'log.db'

    def __init__(self):
        self.db_log = super(DataBaseLogger, self).__init__('log.db')
        self.close_connection = 0
        self.bln_connected = self.connect_to_db(1)

        if (not self._is_table_configured()) and self.bln_connected:
            if not self._create_log_table():
                raise Errors.DataBaseError("Couldn't not create log database.")

    def _is_table_configured(self):
        """
        Check weather the table is created and have data on it.

        Returns:
            True is table exists or have data else False.
        """
        bln_return = True

        try:
            lst_columns = self.get_columns_names(self.tbl_name)

            if lst_columns is None:
                bln_return = False
            else:
                lst_tdata = self.get_table_content(self.tbl_name)

                if lst_tdata:
                    bln_return = True

        except Errors.DataBaseError as excerror:
            lst_tdata = []
            utils.debug(excerror.__str__)

        int_lenght = len(lst_tdata)

        if lst_tdata is None:
            bln_return = False
        elif (lst_tdata is None) or (int_lenght == 0):
            bln_return = False
        return bln_return

    def _create_log_table(self):
        """
        Creates the table for logging purposes.

        Returns:
            True is table has been created, otherwise False
        """
        bln_return = False
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        {lst_columns[0]} VARCHAR(255),  
        {lst_columns[1]} VARCHAR(255), 
        {lst_columns[2]} VARCHAR(255), 
        {lst_columns[3]} VARCHAR(255));""".format(self.tbl_name, lst_columns=self.tbl_columns)

        if self.execute_sql(str_sql) is not None:
            bln_return = True

        return bln_return

    def log_error(self, str_message, str_sql=''):
        """
        Add the log on the table with the current timestamp.

        Args:
            str_message: Message to be added into the table.
            str_sql: SQL tried to execute.

        """

        if not self.bln_connected:
            self.connect_to_db()
        else:
            timestamp = str(int(time()))
            str_date = strftime("%d %b %Y, %H:%M:%S", gmtime())

            if str_sql == '':
                str_sql = "No SQL command."

            if "'" in str_sql:
                str_sql = str_sql.translate(str.maketrans({"'": None}))

            lst_values = utils.convert_list_to_values([str_message, str_sql,
                                                       str_date, str(timestamp)])

            str_sql = """INSERT INTO {} ({lst_columns[0]}, {lst_columns[1]}, {lst_columns[2]},  
            {lst_columns[3]}) VALUES({});""".format(self.tbl_name, lst_values,
                                                    lst_columns=self.tbl_columns)

            self.execute_sql(str_sql)


def print_error(error):
    """
    Nicely print the errors in a descriptive way so it is easier to debug.

    Args:
        error: error of the exception.
    """
    print("==============")
    print("ERROR OCCURRED:")
    print("Date: {}".format(strftime("%d %b %Y, %H:%M:%S", gmtime())))
    print("Error type: {}".format(type(error)))
    print("Arguments: {}".format(error.args))
    print("Error message: {}".format(error.__str__()))
    print("Context: {}".format(error.__context__))
    print("==============")
