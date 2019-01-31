# storage.py

## NAME
storage - Main Storage data management.

## FUNCTIONS

### `add_storage(str_storage, str_location)`
Add storage on the database if the table is configured, if not, create the table and add the
storage passed by parameters.

**Args:**

 * **`str_storage`**  Name for the storage.
 * **`str_location`**  Location of the storage.

**Returns:** True if record is added, else False.


### `get_storages()`
Get all storages on database.

**Returns:** List with the return of get_table_content from Operations.DataBase

## DATA
DB_NAME = 'testing.db'
TBL_STORAGE = 'Storage'
