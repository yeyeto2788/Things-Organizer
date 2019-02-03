"""

Main commons data management for getting data and
logs from different tables.

It also declares the names of the tables.

"""
import time
import inspect

from things_organizer import utils
from things_organizer.db import Operations, Errors

TBL_CATEGORIES = 'Category'
TBL_USERS = 'User'
TBL_USER_THINGS = 'UserThing'
TBL_SESSIONS = 'Session'
TBL_STORAGE = 'Storage'
TBL_THINGS = 'Thing'
TBL_TAGS = 'Tags'
TBL_THINGS_TAGS = 'ThingTag'
DB_NAME = 'testing.db'


def create_tables(str_dbname=DB_NAME):
    """
    Create all tables needed on a given database, by default it is using the 'DB_NAME' which is
    hardcoded in this module.

    Args:
        str_dbname: Name of the database.

    Returns:
        True if all tables where created.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(str_dbname)
    database.close_connection = 0
    database.connect_to_db(1)

    str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
     Name VARCHAR(255) NOT NULL UNIQUE);""".format(TBL_CATEGORIES)
    utils.debug("Executing query \n{}\n".format(str_sql))
    exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Name VARCHAR(255)  NOT NULL UNIQUE, Location VARCHAR(255));""".format(TBL_STORAGE)
        utils.debug("Executing query \n{}\n".format(str_sql))
        exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title VARCHAR(255));""".format(TBL_TAGS)
        utils.debug("Executing query \n{}\n".format(str_sql))
        exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Name VARCHAR(255), Description VARCHAR(255), Unit VARCHAR(30), Quantity INTEGER,
         StorageID INTEGER , CategoryID INTEGER, UNIQUE (ID),
         FOREIGN KEY (StorageID) REFERENCES {}(ID), 
         FOREIGN KEY (CategoryID) REFERENCES {}(ID));
         """.format(TBL_THINGS, TBL_STORAGE, TBL_CATEGORIES)
        utils.debug("Executing query \n{}\n".format(str_sql))
        exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Name VARCHAR(255), Lastname VARCHAR(255),
         Email VARCHAR(255) NOT NULL UNIQUE, Password VARCHAR(255), LastLogin VARCHAR(255),
         Active BIT);""".format(TBL_USERS)
        utils.debug("Executing query \n{}\n".format(str_sql))
        exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         TagID INTEGER, ThingID INTEGER, FOREIGN KEY (TagID) REFERENCES {}(ID),
         FOREIGN KEY (ThingID) REFERENCES {}(ID));""".format(TBL_THINGS_TAGS, TBL_TAGS, TBL_THINGS)
        utils.debug("Executing query \n{}\n".format(str_sql))
        exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         UserID INTEGER, ThingID INTEGER, FOREIGN KEY (UserID) REFERENCES {}(ID),
         FOREIGN KEY (ThingID) REFERENCES {}(ID));""".format(TBL_USER_THINGS, TBL_USERS, TBL_THINGS)
        utils.debug("Executing query \n{}\n".format(str_sql))
        exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        str_sql = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         UserID INTEGER NOT NULL UNIQUE, SessionKey VARCHAR(255) UNIQUE, TimeStamp VARCHAR(255)
         );""".format(TBL_SESSIONS)
        utils.debug("Executing query \n{}\n".format(str_sql))
        exe_return = database.execute_sql(str_sql)
    if exe_return is not None:
        bln_return = True

    database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def is_data_on_table(str_tname, lst_values, bln_omit_id=1):
    """
    Check weather the data is present on table so if already present on table there is no need to
    add more record to the table.

    Args:
        str_tname: Table name.
        lst_values: list with the value to check. (It has to be in order as in the database)
        bln_omit_id: This will omit or not the column id.

    Returns:
        True if data exists on table else False.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    if is_table_configured(str_tname):
        try:
            lst_columns = database.get_columns_names(str_tname)
            if bln_omit_id:
                lst_columns.pop(0)
            cursor = database.db_connection.cursor()
            str_sql = "SELECT {} FROM {} WHERE ".format(utils.convert_list_to_columns(lst_columns),
                                                        str_tname)
            for str_column, value in zip(lst_columns, lst_values):
                str_sql += "{}={} AND ".format(
                    str_column, value if not isinstance(value, str) else "'{}'".format(value))

            if str_sql.endswith(' AND '):
                str_sql = str_sql[:len(str_sql) - 5]

            utils.debug("Executing query \n{}\n".format(str_sql))
            cursor.execute(str_sql)
            rows = cursor.fetchall()
            int_row_length = len(rows)

            if int_row_length > 0:
                bln_return = True

        except Exception as excerror:
            utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
            db_log = Operations.DataBaseLogger()
            db_log.log_error(excerror.__str__(), str_sql)

        finally:
            database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def is_table_configured(str_tname):
    """
    Check weather the table is configured or not, also check that the table has data on it.

    Args:
        str_tname: Table name.

    Returns:
        True if table is configured, else False.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)

    try:

        database.connect_to_db()

        lst_columns = database.get_columns_names(str_tname)

        if lst_columns is None:
            bln_return = False
        else:
            lst_tdata = database.get_table_content(str_tname)

            if lst_tdata:
                bln_return = True

    except Errors.DataBaseExistenceError as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
        bln_return = False

    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def get_all_data_from(str_tname):
    """
    Get all data from a table.

    Args:
        str_tname: Table name.

    Returns:
        List with return of get_table_content from Operations.DataBase

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.connect_to_db()
    lst_return = database.get_table_content(str_tname)
    database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_return


def get_columns_from(str_tname):
    """
    Get all columns names from a given table passed by argument.

    Args:
        str_tname: Table name.

    Returns:
        List with return of get_columns_names from Operations.DataBase.

    """

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.connect_to_db()
    lst_return = database.get_columns_names(str_tname)
    database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_return


def get_data_by_id(str_tname, int_id):
    """
    Get the columns values based on the ID passed by argument to the function performing a
    `SELECT * FROM str_tname WHERE ID=int_id;`.

    Args:
        str_tname: Table name.
        int_id: id from which we'll request data from.

    Returns:
        List with the return for the sqlite3 cursor.execute, in case of failure list will be empty.

    """

    lst_return = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.connect_to_db()
    cursor = database.db_connection.cursor()
    str_sql = "SELECT * FROM {} WHERE ID={};".format(str_tname, int_id)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        for row in cursor.execute(str_sql):
            lst_return = [column for column in row]
    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_return


def get_logs():
    """
    Extract all application logs into a list.

    Returns:
        List with all values if exists on database.

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBaseLogger()

    try:
        lst_data = database.get_table_content(database.tbl_name)

    except Errors.DataBaseError as excerror:
        utils.debug(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data


def update_table_row(str_tname, lst_columns, lst_values, int_id=None):
    """
    Edits the information on a table based on the ID and also the new values passed by arguments.

    Args:
        str_tname: Table name.
        lst_columns: Columns to be changed.
        lst_values: values to be inserted.
        int_id: Id of the row to be edited.

    Returns:
        Boolean with the return of execute_sql from Operations.DataBase.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    if ('ID' in lst_columns) and (int_id is not None) and (len(lst_columns) == len(lst_values)):
        int_remove = lst_columns.index('ID')
        lst_columns.pop(int_remove)
        lst_values.pop(int_remove)
        str_sql_where = "WHERE ID={id};".format(id=int_id)
    elif ('ID' in lst_columns) and (int_id is not None) and (len(lst_columns) > len(lst_values)):
        int_remove = lst_columns.index('ID')
        lst_columns.pop(int_remove)
        str_sql_where = "WHERE ID={id};".format(id=int_id)
    elif ('ID' in lst_columns) and isinstance(int_id, int) and (len(lst_columns) > len(lst_values)):
        int_remove = lst_columns.index('ID')
        lst_columns.pop(int_remove)
        str_sql_where = "WHERE ID={id};".format(id=int_id)
    # TODO: elif with request id from db in case no passed through arguments
    else:
        return bln_return

    str_assignment = utils.convert_lists_to_assignment(lst_columns, lst_values)
    str_sql = "UPDATE {table_name} SET {assign} {where}".format(table_name=str_tname,
                                                                assign=str_assignment,
                                                                where=str_sql_where)
    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        bln_return = database.execute_sql(str_sql)

    except Errors.DataBaseError as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)

    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return
