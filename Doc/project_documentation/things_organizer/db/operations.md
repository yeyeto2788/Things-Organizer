# operations.py

## NAME
operations - Main database operations are done at this level.

## CLASSES
builtins.object
DataBase
DataBaseLogger


### `class DataBase(builtins.object)`

### `DataBase(str_db_name='things_organizer.db')`

Database object to do all possible operation on DB.

Attributes:
 * **`close_connection`**  whether to close or not after each operation.
 * **`str_db_name`**  Name of the database.
 * **`db_connection`**  Connection from `sqlite3.connect`

Methods defined here:


### `__init__(self, str_db_name='things_organizer.db')`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `close_db_connection(self)`
Close connection if present, otherwise an error will be raised.

**Returns:** True if connection closed, else False.


### `connect_to_db(self, bln_create_db=0)`
Connect to the database, by default if no name was given at the moment of the
instance creation it will automatically connect to 'things_organizer.db'.

**Returns:** True if connection OK, else False


### `create_table(self, str_tname, lst_columns)`
Create a table from the create_table_sql statement.

**Args:**

 * **`str_tname`**  Table name to be created.
 * **`lst_columns`**  Columns to be added.

**Returns:** True if table created, else False.


### `drop_table(self, str_tname)`
Deletes a given table from the database.

**Args:**

 * **`str_tname`**  Table name.

**Returns:** True if table was dropped, else `None`


### `execute_sql(self, str_command)`
Executes any kind of query on the database.

**Args:**

 * **`str_command`**  Command to be executed.

**Returns:** `None` if an error occurs on execution, else True


### `get_columns_names(self, str_tname)`
Get the table column's names of a given table by the return of the `cursor.description`.

**Args:**

 * **`str_tname`**  Name of the table.

**Returns:** List with the columns names. otherwise `None` will be returned.


### `get_db_tables(self)`
Get all tables on the database.

**Returns:** List with the name of the table, if error is raised on execution a `None` will be
returned.


### `get_table_content(self, str_tname)`
Perform a `SELECT * FROM <str_tname>` and return its result.

**Args:**

 * **`str_tname`**  Name of table to retrieve data from.

**Returns:** List with table data if the table exists on `db` directory.


### `insert_into_table(self, str_tname, lst_values)`
Insert values into a given table.

**Args:**

 * **`str_tname`**  Table name where data will be inserted.
 * **`lst_values`**  values to be inserted.

**Returns:** Integer of the row inserted, otherwise a `None` will be returned.


Data descriptors defined here:

__dict__
dictionary for instance variables (if defined)

__weakref__
list of weak references to the object (if defined)


Data and other attributes defined here:

close_connection = 1


### `class DataBaseLogger(DataBase)`
Database object to log all failures of the application.

Attributes:
 * **`tbl_name`**  Table name.
 * **`tbl_columns`**  Name for the columns used in the table.
 * **`db_name`**  Name for specific loggin db.
 * **`db_log`**  instance of the Database.

Method resolution order:
DataBaseLogger
DataBase
builtins.object

Methods defined here:


### `__init__(self)`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `log_error(self, str_message, str_sql='')`
Add the log on the table with the current timestamp.

**Args:**

 * **`str_message`**  Message to be added into the table.
 * **`str_sql`**  SQL tried to execute.


Data and other attributes defined here:

db_name = 'log.db'

tbl_columns = ['Message', 'strSQL', 'Date', 'Timestamp']

tbl_name = 'Logs'


Methods inherited from DataBase:


### `close_db_connection(self)`
Close connection if present, otherwise an error will be raised.

**Returns:** True if connection closed, else False.


### `connect_to_db(self, bln_create_db=0)`
Connect to the database, by default if no name was given at the moment of the
instance creation it will automatically connect to 'things_organizer.db'.

**Returns:** True if connection OK, else False


### `create_table(self, str_tname, lst_columns)`
Create a table from the create_table_sql statement.

**Args:**

 * **`str_tname`**  Table name to be created.
 * **`lst_columns`**  Columns to be added.

**Returns:** True if table created, else False.


### `drop_table(self, str_tname)`
Deletes a given table from the database.

**Args:**

 * **`str_tname`**  Table name.

**Returns:** True if table was dropped, else `None`


### `execute_sql(self, str_command)`
Executes any kind of query on the database.

**Args:**

 * **`str_command`**  Command to be executed.

**Returns:** `None` if an error occurs on execution, else True


### `get_columns_names(self, str_tname)`
Get the table column's names of a given table by the return of the `cursor.description`.

**Args:**

 * **`str_tname`**  Name of the table.

**Returns:** List with the columns names. otherwise `None` will be returned.


### `get_db_tables(self)`
Get all tables on the database.

**Returns:** List with the name of the table, if error is raised on execution a `None` will be
returned.


### `get_table_content(self, str_tname)`
Perform a `SELECT * FROM <str_tname>` and return its result.

**Args:**

 * **`str_tname`**  Name of table to retrieve data from.

**Returns:** List with table data if the table exists on `db` directory.


### `insert_into_table(self, str_tname, lst_values)`
Insert values into a given table.

**Args:**

 * **`str_tname`**  Table name where data will be inserted.
 * **`lst_values`**  values to be inserted.

**Returns:** Integer of the row inserted, otherwise a `None` will be returned.


Data descriptors inherited from DataBase:

__dict__
dictionary for instance variables (if defined)

__weakref__
list of weak references to the object (if defined)


Data and other attributes inherited from DataBase:

close_connection = 1

## FUNCTIONS

### `gmtime(...)`

### `gmtime([seconds]) -> (tm_year, tm_mon, tm_mday, tm_hour, tm_min,`
tm_sec, tm_wday, tm_yday, tm_isdst)

Convert seconds since the Epoch to a time tuple expressing UTC (a.k.a.
GMT).  When 'seconds' is not passed in, convert the current time instead.

If the platform supports the tm_gmtoff and tm_zone, they are available as
attributes only.


### `print_error(error)`
Nicely print the errors in a descriptive way so it is easier to debug.

**Args:**

 * **`error`**  error of the exception.


### `strftime(...)`

### `strftime(format[, tuple]) -> string`

Convert a time tuple to a string according to a format specification.
See the library reference manual for formatting codes. When the time tuple

### `is not present, current time as returned by localtime() is used.`

Commonly used format codes:

%Y  Year with century as a decimal number.
%m  Month as a decimal number [01,12].
%d  Day of the month as a decimal number [01,31].
%H  Hour (24-hour clock) as a decimal number [00,23].
%M  Minute as a decimal number [00,59].
%S  Second as a decimal number [00,61].
%z  Time zone offset from UTC.
%a  Locale's abbreviated weekday name.
%A  Locale's full weekday name.
%b  Locale's abbreviated month name.
%B  Locale's full month name.
%c  Locale's appropriate date and time representation.
%I  Hour (12-hour clock) as a decimal number [01,12].
%p  Locale's equivalent of either AM or PM.

Other codes may be available on your platform.  See documentation for
the C library strftime function.


### `time(...)`

### `time() -> floating point number`

Return the current time in seconds since the Epoch.
Fractions of a second may be present if the system clock provides them.

## DATA
DB_PATH = r'C:\workspace\unnamed\things_organizer\data'
