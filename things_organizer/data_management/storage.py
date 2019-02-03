"""

Main Storage data management.

"""
import time
import inspect

from things_organizer import utils
from things_organizer.data_management.common import DB_NAME, is_table_configured, TBL_STORAGE
from things_organizer.db import Operations, Errors


def add_storage(str_storage, str_location):
    """
    Add storage on the database if the table is configured, if not, create the table and add the
    storage passed by parameters.

    Args:
        str_storage: Name for the storage.
        str_location: Location of the storage.

    Returns:
        True if record is added, else False.
    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db(1)
    lst_cnames = ['Name', 'Location']

    if is_table_configured(TBL_STORAGE):
        if str_storage != '':
            str_sql = """
            INSERT INTO {} ({}) VALUES('{}', '{}');""".format(TBL_STORAGE,
                                                              utils.convert_list_to_columns(
                                                                  lst_cnames),
                                                              str_storage, str_location)

            try:
                utils.debug("Executing query \n{}\n".format(str_sql))
                if database.execute_sql(str_sql) is not None:
                    bln_return = True
            except Errors.DataBaseError as excerror:
                utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
                db_log = Operations.DataBaseLogger()
                db_log.log_error(excerror.__str__(), str_sql)
            finally:
                database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def get_storages():
    """
    Get all storages on database.

    Returns:
        List with the return of get_table_content from Operations.DataBase

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.connect_to_db()

    try:
        utils.debug("Getting all data from table {}\n".format(TBL_STORAGE))
        lst_data = database.get_table_content(TBL_STORAGE)
    except Errors.DataBaseError as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data


def get_storage_id(str_name):
    """
    Get the id of the storage based on the name of the storage.

    Args:
        str_name: Name of the storage.

    Returns:
        int if found, else None
    """

    int_return = None

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()
    cursor = database.db_connection.cursor()

    str_sql = "SELECT ID FROM {} WHERE Name='{}'".format(TBL_STORAGE, str_name)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        cursor.execute(str_sql)
        rows = cursor.fetchall()
        int_row_length = len(rows)

        if int_row_length > 0:
            for row in rows:
                for column in row:
                    int_return = column
                    break
                break
    except Errors.DataBaseError as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return int_return
