# user.py

## NAME
user - Main User data management.

## FUNCTIONS

### `add_session(int_user)`
Insert a new session key on the database and if there is one that didn't get deleted, delete it
and create a new one.

**Args:**

 * **`int_user`**  User ID.

**Returns:** True if operation is done, else False.


### `check_session(int_user)`
Verify that the time of the session is still within the normal usage of the application.

If time is over, it will delete the session from the database.

**Args:**

 * **`int_user`**  User id.

**Returns:** Boolean with the result of operation done.


### `delete_all_sessions()`
Delete all sessions from the database.

**Returns:** True if deletion successful, else False.


### `delete_session(int_id)`
Delete a session from the database.

**Args:**

 * **`int_id`**  User id.

**Returns:** True if deletion successful, else False.


### `get_session(int_user)`
Look on the database the session key of the given user.

**Args:**

 * **`int_user`**  User id.

**Returns:** string with session key if found, else None.


### `get_user_id(str_email)`
Get the user id from the database.

**Args:**

 * **`str_email`**  User email.

**Returns:** Integer with id if found, else None


### `get_user_password(str_email)`
Get from the database the password of the user.

**Args:**

 * **`str_email`**  email of the user to look the password of.

**Returns:** string with the password.


### `is_user(str_email, str_password)`
Check whether the user exists on the database.

**Args:**

 * **`str_email`**  Email to look for in the database.
str_password:

**Returns:** True if found, else False.


### `register_user(str_name, str_lastname, str_email, str_password)`
Adds the user into the database.

**Args:**

 * **`str_name`**  Name of the user.
 * **`str_lastname`**  Last name of the user.
 * **`str_email`**  Email
 * **`str_password`**  Password.

**Returns:** True if successful, else False.

## DATA
DB_NAME = 'testing.db'

TBL_SESSIONS = 'Session'

TBL_USERS = 'User'
