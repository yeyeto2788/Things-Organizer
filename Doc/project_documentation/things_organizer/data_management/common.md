# common.py

## NAME
common

## DESCRIPTION
Main commons data management for getting data and
logs from different tables.

It also declares the names of the tables.

## FUNCTIONS

### `create_tables(str_dbname='testing.db')`
Create all tables needed on a given database, by default it is using the 'DB_NAME' which is
hardcoded in this module.

**Args:**

 * **`str_dbname`**  Name of the database.

**Returns:** True if all tables where created.


### `exists_database()`
Check whether the database exists or not on the given path for database operations.

**Returns:** True if database, else False.


### `get_all_data_from(str_tname)`
Get all data from a table.

**Args:**

 * **`str_tname`**  Table name.

**Returns:** List with return of get_table_content from Operations.DataBase


### `get_columns_from(str_tname)`
Get all columns names from a given table passed by argument.

**Args:**

 * **`str_tname`**  Table name.

**Returns:** List with return of get_columns_names from Operations.DataBase.


### `get_data_by_id(str_tname, int_id)`
Get the columns values based on the ID passed by argument to the function performing a
`SELECT * FROM str_tname WHERE ID=int_id;`.

**Args:**

 * **`str_tname`**  Table name.
 * **`int_id`**  id from which we'll request data from.

**Returns:** List with the return for the sqlite3 cursor.execute, in case of failure list will be empty.


### `get_logs()`
Extract all application logs into a list.

**Returns:** List with all values if exists on database.


### `is_data_on_table(str_tname, lst_values, bln_omit_id=1)`
Check weather the data is present on table so if already present on table there is no need to
add more record to the table.

**Args:**

 * **`str_tname`**  Table name.
 * **`lst_values`**  list with the value to check. (It has to be in order as in the database)
 * **`bln_omit_id`**  This will omit or not the column id.

**Returns:** True if data exists on table else False.


### `is_table_configured(str_tname)`
Check weather the table is configured or not, also check that the table has data on it.

**Args:**

 * **`str_tname`**  Table name.

**Returns:** True if table is configured, else False.


### `update_table_row(str_tname, lst_columns, lst_values, int_id=None)`
Edits the information on a table based on the ID and also the new values passed by arguments.

**Args:**

 * **`str_tname`**  Table name.
 * **`lst_columns`**  Columns to be changed.
 * **`lst_values`**  values to be inserted.
 * **`int_id`**  Id of the row to be edited.

**Returns:** Boolean with the return of execute_sql from Operations.DataBase.

## DATA
DB_NAME = 'testing.db'
TBL_CATEGORIES = 'Category'
TBL_SESSIONS = 'Session'
TBL_STORAGE = 'Storage'
TBL_TAGS = 'Tags'
TBL_THINGS = 'Thing'
TBL_THINGS_TAGS = 'ThingTag'
TBL_USERS = 'User'
TBL_USER_THINGS = 'UserThing'
