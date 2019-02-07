# tag.py

## NAME
tag - Main Tag data management.

## FUNCTIONS

### `add_tag(str_tag_title)`
Add tag on the database.

**Args:**

 * **`str_tag_title`**  Title/Name of the tag.

**Returns:** True if record is added, else False.


### `get_tags()`
Get all tags on database.

**Returns:** List with the return of get_table_content from Operations.DataBase

## DATA
DB_NAME = 'testing.db'

TBL_TAGS = 'Tags'
