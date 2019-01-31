# utils.py

## NAME
utils

## DESCRIPTION
Utils module to use all over the application in order
not to repeat code.

Common conversions and so on.

## FUNCTIONS

### `convert_list_to_columns(lst_columns)`
Convert list type into string for sql column purposes.

**Args:**

 * **`lst_columns`**  columns to be converted.

**Returns:** String with the columns converted.


### `convert_list_to_values(lst_values)`
Convert list type into string values for sql purposes.

**Args:**

 * **`lst_values`**  values to be converted.

**Returns:** String with the values converted.


### `convert_lists_to_assignment(lst_columns, lst_values)`
For a given list of values convert it into SQL string assignment.

**Args:**

 * **`lst_columns`**  List of columns to which values will be assigned.
 * **`lst_values`**  List of values to be assigned.

**Returns:** String with the SQL assignment like <column>='<value>'.


### `debug(*args, **kargs)`
wrapper to print values on the terminal in case debug mode is enable.

**Args:**

 * **`*args`**  Arguments for the print function.
 * **`**kargs`**  Keyword arguments to the print function.


### `generate_session()`
Generate a seudo random session key for database filling.

**Returns:** String with the session key.


### `sort_alphanumeric_list(lst_unsorted)`
Sorts the given iterable in the way that is expected.

**Args:**

 * **`lst_unsorted`**  List of values to be sorted.

**Returns:** Same list sorted.


### `str_to_bln(str_value)`
Convert a given string based on ('y', 'yes', 't', 'true', 'on', '1') into a boolean.

An `ValueError` might be raised if not possible to convert string to boolean.

**Args:**

 * **`str_value`**  Value to be converted

**Returns:** True if possible to convert. otherwise False.


### `urandom(size, /)`
Return a bytes object containing random bytes suitable for cryptographic use.
