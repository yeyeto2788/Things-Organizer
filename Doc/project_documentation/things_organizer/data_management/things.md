# things.py

## NAME
things - Main Things data management.

## FUNCTIONS

### `add_thing()`
Add a new thing into the database and populate needed tables.

**Returns:** True if operation done, else False.


### `get_thing_tags(int_thingid)`
Get all tags assigned to an specific thing. It will look on the database all tags for that
given thing id.

**Args:**

 * **`int_thingid`**  Id of the thing to look the tags for.

**Returns:** list of tag titles if there is any tag assigned to the thing.


### `get_things_by_category(str_category, int_user)`
Obtain all things belonging to a user by a given category name.

**Args:**

 * **`str_category`**  Category to look thing of.
 * **`int_user`**  User ID.

**Returns:** List with the query executed.


### `get_things_by_location(str_location, int_user)`
Obtain all things belonging to a user by a given location.

**Args:**

 * **`str_location`**  Location to look things on.
 * **`int_user`**  User ID.

**Returns:** List with the query executed.


### `get_things_by_storage(str_storage, int_user)`
Obtain all things belonging to a user by a given storage.

**Args:**

 * **`str_storage`**  Storage to look things on.
 * **`int_user`**  User ID.

**Returns:** List with the query executed.


### `get_user_things(int_id)`
Get all things that belongs to a given user ID

**Args:**

 * **`int_id`**  User id.

**Returns:** List with available rows of data.

## DATA
DB_NAME = 'testing.db'
TBL_CATEGORIES = 'Category'
TBL_STORAGE = 'Storage'
TBL_TAGS = 'Tags'
TBL_THINGS = 'Thing'
TBL_THINGS_TAGS = 'ThingTag'
TBL_USER_THINGS = 'UserThing'
