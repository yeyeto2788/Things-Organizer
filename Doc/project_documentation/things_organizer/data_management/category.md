# category.py

## NAME
category - Main Category data management.

## FUNCTIONS

### `add_category(str_category)`
Adds a category on the table if table is configured, if table is not configured it will create
the table on the given database and add the category on it.

**Args:**

 * **`str_category`**  Category to be added.

**Returns:** True if record added, else False.


### `get_categories()`
Get all categories on database.

**Returns:** List with the return of get_table_content from Operations.DataBase


### `get_category_id(str_name)`
Get the id of the category based on the name of the storage.

**Args:**

 * **`str_name`**  Name of the storage.

**Returns:** int if found, else None

## DATA
DB_NAME = 'testing.db'

TBL_CATEGORIES = 'Category'
