"""

Main Things data management.

"""
import time
import inspect

from things_organizer import utils
from things_organizer.data_management.common import DB_NAME, TBL_TAGS, TBL_THINGS_TAGS, TBL_THINGS
from things_organizer.data_management.common import TBL_STORAGE, TBL_CATEGORIES, TBL_USER_THINGS
from things_organizer.data_management.common import get_columns_from
from things_organizer.db import Operations, Errors


def add_thing(lst_columns, lst_values, int_user):
    """
    Add a new thing into the database and also link thing to user given by
    argument.

    Args:
        lst_columns: Columns to be added on the sql
        lst_values: Values to be assigned
        int_user: User id

    Returns:
        True if operation done, else False.

    """

    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()
    cursor = database.db_connection.cursor()

    str_sql = "INSERT INTO {table_name} ({columns}) VALUES({values});".format(
        table_name=TBL_THINGS,
        values=utils.convert_list_to_values(lst_values),
        columns=utils.convert_list_to_columns(lst_columns))

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        cursor.execute(str_sql)

        # Retrieve last inserted row.
        int_thing = cursor.lastrowid

        bln_return = add_user_thing(int_thing, int_user)

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__(), str_sql)

    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return bln_return


def add_user_thing(int_user, int_thing):
    """
    Assign a thing to a user.

    Args:
        int_user: User Id
        int_thing: Thing Id

    Returns:
        True if operation done, else False.
    """
    bln_return = False

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    lst_columns = get_columns_from(TBL_USER_THINGS)[1:]

    str_sql = "INSERT INTO {table_name} ({columns}) VALUES({values});".format(
        table_name=TBL_USER_THINGS,
        values=utils.convert_list_to_values([int_user, int_thing]),
        columns=utils.convert_list_to_columns(lst_columns))

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


def get_thing_tags(int_thingid):
    """
    Get all tags assigned to an specific thing. It will look on the database all tags for that
    given thing id.

    Args:
        int_thingid: Id of the thing to look the tags for.

    Returns:
        list of tag titles if there is any tag assigned to the thing.

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    cursor = database.db_connection.cursor()
    str_sql = """
    SELECT Title FROM {tags} JOIN {thingtags} ON {tags}.ID = {thingtags}.TagID
     JOIN Things ON {thingtags}.ID = {thing}.ID WHERE {thing}.ID = {}
    """.format(int_thingid, tags=TBL_TAGS, thingtags=TBL_THINGS_TAGS, thing=TBL_THINGS)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        for row in cursor.execute(str_sql):
            lst_data = [column for column in row]
    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data


def get_things_by_category(str_category, int_user):
    """
    Obtain all things belonging to a user by a given category name.

    Args:
        str_category: Category to look thing of.
        int_user: User ID.

    Returns:
        List with the query executed.

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    cursor = database.db_connection.cursor()

    str_sql = """SELECT {thing}.Name, {thing}.Description,
    {storage}.Name As Storage, {storage}.Location As Location,
    {thing}.Unit, {thing}.Quantity
    FROM {thing} 
    JOIN {storage} ON {thing}.StorageID = {storage}.ID 
    JOIN {userthing} ON {thing}.ID = {userthing}.ThingID
    JOIN {cat} ON {thing}.CategoryID = {cat}.ID
    WHERE {cat}.Name = '{}' AND {userthing}.UserID = {}
    """.format(str_category, int_user, thing=TBL_THINGS, storage=TBL_STORAGE, cat=TBL_CATEGORIES,
               userthing=TBL_USER_THINGS)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        rows = cursor.execute(str_sql)

        if rows:

            for row in rows:
                lst_data.append([column for column in row])

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data


def get_things_by_location(str_location, int_user):
    """
    Obtain all things belonging to a user by a given location.

    Args:
        str_location: Location to look things on.
        int_user: User ID.

    Returns:
        List with the query executed.

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    cursor = database.db_connection.cursor()

    str_sql = """SELECT {thing}.Name, {thing}.Description,
    {cat}.Name AS Category, {storage}.Name As Storage,
    {thing}.Unit, {thing}.Quantity,
    FROM {thing} 
    JOIN {storage} ON {thing}.StorageID = {storage}.ID 
    JOIN {userthing} ON {thing}.ID = {userthing}.ThingID
    JOIN {cat} ON {thing}.CategoryID = {cat}.ID
    WHERE {storage}.Location = '{}' AND {userthing}.UserID = {};
    """.format(str_location, int_user, thing=TBL_THINGS, storage=TBL_STORAGE, cat=TBL_CATEGORIES,
               userthing=TBL_USER_THINGS)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        rows = cursor.execute(str_sql)

        if rows:

            for row in rows:
                lst_data.append([column for column in row])

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data


def get_things_by_storage(str_storage, int_user):
    """
    Obtain all things belonging to a user by a given storage.

    Args:
        str_storage: Storage to look things on.
        int_user: User ID.

    Returns:
        List with the query executed.

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.close_connection = 0
    database.connect_to_db()

    cursor = database.db_connection.cursor()

    str_sql = """SELECT {thing}.Name, {thing}.Description,
    {cat}.Name AS Category,
    {thing}.Unit, {thing}.Quantity
    FROM {thing} 
    JOIN {storage} ON {thing}.StorageID = {storage}.ID 
    JOIN {userthing} ON {thing}.ID = {userthing}.ThingID
    JOIN {cat} ON {thing}.CategoryID = {cat}.ID
    WHERE {storage}.Name = '{}' AND {userthing}.UserID = {}
    """.format(str_storage, int_user, thing=TBL_THINGS, storage=TBL_STORAGE, cat=TBL_CATEGORIES,
               userthing=TBL_USER_THINGS)

    try:
        utils.debug("Executing query \n{}\n".format(str_sql))
        rows = cursor.execute(str_sql)

        if rows:

            for row in rows:
                lst_data.append([column for column in row])

    except Exception as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())
    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data


def get_user_things(int_id):
    """
    Get all things that belongs to a given user ID

    Args:
        int_id: User id.

    Returns:
        List with available rows of data.

    """

    lst_data = []

    utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    database = Operations.DataBase(DB_NAME)
    database.connect_to_db()
    cursor = database.db_connection.cursor()

    str_sql = """SELECT {thing}.ID, {thing}.Name, {thing}.Description, {thing}.Unit,
     {thing}.Quantity, {storage}.Location AS Location, {storage}.Name AS Storage,
     {cat}.Name AS Category
     FROM {thing}
     JOIN {user_t} ON {thing}.ID = {user_t}.ThingID
     JOIN {storage} ON {thing}.StorageID={storage}.ID
     JOIN {cat} ON {thing}.CategoryID={cat}.ID
     WHERE {user_t}.UserID={id}""".format(id=int_id, thing=TBL_THINGS, cat=TBL_CATEGORIES,
                                          user_t=TBL_USER_THINGS, storage=TBL_STORAGE)

    try:

        utils.debug("Executing query \n{}\n".format(str_sql))
        cursor.execute(str_sql)
        rows = cursor.fetchall()

        for row in rows:
            lst_inner = []
            for column in row:
                lst_inner.append(column)
            lst_data.append(lst_inner)

    except Errors.DataBaseError as excerror:
        utils.debug("An Error occurred: \n {}".format(excerror.__str__()))
        db_log = Operations.DataBaseLogger()
        db_log.log_error(excerror.__str__())

    finally:
        database.close_db_connection()

    utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                              time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

    return lst_data
