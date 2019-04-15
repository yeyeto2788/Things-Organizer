# utils.py

## NAME
utils

## DESCRIPTION
Utils module to use all over the application in order
not to repeat code.

Common conversions and so on.

## FUNCTIONS

### `debug(*args, **kargs)`
wrapper to print values on the terminal in case debug mode is enable.

**Args:**

 * **`*args`** Arguments for the print function.
 * **`**kargs`** Keyword arguments to the print function.


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


### `zip_dir(zip_directory, zip_name, str_directory, bln_delete=0)`
Generate a `.zip` folder with all content on a directory.

**Args:**

 * **`zip_directory`**  Directory where `.zip` file will be saved.
 * **`zip_name`**  Name for the `.zip` folder.
 * **`str_directory`**  Directory to look files from.
 * **`bln_delete`**  Delete previous runs.

**Returns:** Name of the `.zip` folder if generated, else empty string.

## DATA
DB_PATH

LABEL_PATH

REPORT_PATH
