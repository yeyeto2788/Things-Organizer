"""

Main Category data management.

"""
import time
import inspect

from things_organizer import utils
from things_organizer.data_management.common import DB_NAME, is_table_configured, TBL_CATEGORIES
from things_organizer.db import Operations, Errors


def add_category(str_category):
    """
    Adds a category on the table if table is configured, if table is not configured it will create
    the table on the given database and add the category on it.

    Args:
        str_category: Category to be added.

    Returns:
        True if record added, else False.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                       time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    lst_cnames = ['Name']

    database.connect_to_db(1)
    if is_table_configured(TBL_CATEGORIES):
        if str_category != '':
            str_sql = """
            INSERT INTO {} ({}) VALUES('{}');""".format(TBL_CATEGORIES,
                                                        utils.convert_list_to_columns(lst_cnames),
                                                        str_category)
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


def get_categories():
    """
    Get all categories on database.

    Returns:
        List with the return of get_table_content from Operations.DataBase

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                       time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.connect_to_db()

    try:
        lst_data = database.get_table_content(TBL_CATEGORIES)
    except Errors.DataBaseError as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                       time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data
