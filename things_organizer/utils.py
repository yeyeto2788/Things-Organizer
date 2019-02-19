"""
Utils module to use all over the application in order
not to repeat code.

Common conversions and so on.

"""
import os
import re

from os import urandom
from base64 import b64encode


DB_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "db"))


def convert_lists_to_assignment(lst_columns, lst_values):
    """
    For a given list of values convert it into SQL string assignment.

    Args:
        lst_columns: List of columns to which values will be assigned.
        lst_values: List of values to be assigned.

    Returns:
        String with the SQL assignment like <column>='<value>'.

    """

    str_assignment = ""

    for int_counter, (column, value) in enumerate(zip(lst_columns, lst_values)):

        if isinstance(value, int):
            str_value = "{}".format(value)
        else:
            str_value = "'{}'".format(value)

        if int_counter != (len(lst_columns) - 1):
            str_assignment += "{}={}, ".format(column, str_value)
        else:
            str_assignment += "{}={} ".format(column, str_value)

    return str_assignment


def convert_list_to_columns(lst_columns):
    """
    Convert list type into string for sql column purposes.

    Args:
        lst_columns: columns to be converted.

    Returns:
        String with the columns converted.

    """

    str_columns = ""

    for int_counter, str_column in enumerate(lst_columns):
        if int_counter != (len(lst_columns) - 1):
            str_columns += "{}, ".format(str_column)
        else:
            str_columns += "{} ".format(str_column)

    return str_columns


def convert_list_to_values(lst_values):
    """
    Convert list type into string values for sql purposes.

    Args:
        lst_values: values to be converted.

    Returns:
        String with the values converted.

    """

    str_values = ""

    for int_counter, value in enumerate(lst_values):

        if int_counter != (len(lst_values) - 1):
            if not isinstance(value, int):
                str_values += "'{}', ".format(value)
            else:
                str_values += "{}, ".format(value)
        else:
            str_values += "{} ".format(value)

    return str_values


def debug(*args, **kargs):
    """
    wrapper to print values on the terminal in case debug mode is enable.

    Args:
        *args: Arguments for the print function.
        **kargs: Keyword arguments to the print function.

    """
    # TODO: change value of bln_print to take it from a config file.
    bln_print = 1

    if bln_print:
        print(*args, **kargs)


def sort_alphanumeric_list(lst_unsorted):
    """
    Sorts the given iterable in the way that is expected.

    Args:
        lst_unsorted: List of values to be sorted.

    Returns:
        Same list sorted.

    """

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(lst_unsorted, key=alphanum_key)


def str_to_bln(str_value):
    """
    Convert a given string based on ('y', 'yes', 't', 'true', 'on', '1') into a boolean.

    An `ValueError` might be raised if not possible to convert string to boolean.

    Args:
        str_value: Value to be converted

    Returns:
        True if possible to convert. otherwise False.

    """

    val = str_value.lower()

    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        bln_return = True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        bln_return = False
    else:
        raise ValueError("{} is not compatible to convert into boolean.".format(str_value))
    return bln_return


def generate_session():
    """
    Generate a seudo random session key for database filling.

    Returns:
        String with the session key.

    """

    str_return = b64encode(urandom(16)).decode('utf-8')
    return str_return
