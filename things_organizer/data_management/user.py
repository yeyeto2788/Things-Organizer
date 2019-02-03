"""

Main User data management.

"""
import inspect
import time

from things_organizer import utils
from things_organizer.data_management.common import DB_NAME, TBL_SESSIONS, TBL_USERS
from things_organizer.db import Operations, Errors


def add_session(int_user):
    """
    Insert a new session key on the database and if there is one that didn't get deleted, delete it
    and create a new one.

    Args:
        int_user: User ID.

    Returns:
        True if operation is done, else False.

    """
    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    str_previous = get_session(int_user)

    if str_previous is not None:
        delete_session(int_user)

    str_session = utils.generate_session()
    str_timestamp = "{}".format(int(time.time()))

    str_sql = """INSERT INTO {} (SessionKey, Timestamp, UserID) 
    VALUES('{}', '{}', {})""".format(TBL_SESSIONS, str_session, str_timestamp, int_user)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        bln_return = database.execute_sql(str_sql)
    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def is_user(str_email, str_password):
    """
    Check whether the user exists on the database.

    Args:
        str_email: Email to look for in the database.
        str_password:

    Returns:
        True if found, else False.
    """
    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()
    cursor = database.db_connection.cursor()

    str_sql = "SELECT ID FROM {} WHERE Email='{}' AND Password='{}'".format(TBL_USERS, str_email,
                                                                            str_password)

    try:

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


def delete_all_sessions():
    """
    Delete all sessions from the database.

    Returns:
        True if deletion successful, else False.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    str_sql = """DELETE FROM {}""".format(TBL_SESSIONS)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        bln_return = database.execute_sql(str_sql)
    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def delete_session(int_id):
    """
    Delete a session from the database.

    Args:
        int_id: User id.

    Returns:
        True if deletion successful, else False.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    str_sql = """DELETE FROM {} WHERE UserID={}""".format(TBL_SESSIONS, int_id)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        bln_return = database.execute_sql(str_sql)
    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def get_session(int_user):
    """
    Look on the database the session key of the given user.

    Args:
        int_user: User id.

    Returns:
        string with session key if found, else None.

    """

    str_session = None

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db(0)
    cursor = database.db_connection.cursor()

    str_sql = """SELECT SessionKey FROM {} WHERE UserID={}""".format(TBL_SESSIONS, int_user)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        cursor.execute(str_sql)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                for column in row:
                    str_session = column
                    break
                break

        else:
            str_session = None

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return str_session


def get_user_id(str_email):
    """
    Get the user id from the database.

    Args:
        str_email: User email.

    Returns:
        Integer with id if found, else None

    """

    int_return = None

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()
    cursor = database.db_connection.cursor()

    str_sql = "SELECT ID FROM {} WHERE Email='{}'".format(TBL_USERS, str_email)

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

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return int_return


def get_user_password(str_email):
    """
    Get from the database the password of the user.

    Args:
        str_email: email of the user to look the password of.

    Returns:
        string with the password.

    """

    str_return = None

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()
    cursor = database.db_connection.cursor()

    str_sql = "SELECT Password FROM {} WHERE Email='{}'".format(TBL_USERS, str_email)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        cursor.execute(str_sql)
        rows = cursor.fetchall()
        int_row_length = len(rows)

        if int_row_length > 0:
            for row in rows:
                for column in row:
                    str_return = column
                    break
                break

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)

    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return str_return


def register_user(str_name, str_lastname, str_email, str_password):
    """
    Adds the user into the database.

    Args:
        str_name: Name of the user.
        str_lastname: Last name of the user.
        str_email: Email
        str_password: Password.

    Returns:
        True if successful, else False.
    """
    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    str_sql = """INSERT INTO {user} (Name, Lastname, Email, Password, LastLogin, Active)
     VALUES('{name}', '{lastname}', '{email}', '{password}', '{timestamp}', 1);
     """.format(user=TBL_USERS, name=str_name, lastname=str_lastname, email=str_email,
                password=str_password, timestamp=int(time.time()))
    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        bln_return = database.execute_sql(str_sql)

    except Errors.AlreadyExistsError as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def check_session(int_user):
    """
    Verify that the time of the session is still within the normal usage of the application.

    If time is over, it will delete the session from the database.

    Args:
        int_user: User id.

    Returns:
        Boolean with the result of operation done.

    """
    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db(0)
    cursor = database.db_connection.cursor()

    str_sql = """SELECT Timestamp FROM {} WHERE UserID={}""".format(TBL_SESSIONS, int_user)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        cursor.execute(str_sql)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                for column in row:
                    int_db_time = int(column)
                    current_time = int(time.time())

                    if (current_time - int_db_time) >= 60 * 10:
                        delete_session(int_user)
                    else:
                        bln_return = True
                    break
                break

        else:
            bln_return = False

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return
