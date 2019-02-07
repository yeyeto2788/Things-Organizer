# main_app.py

## NAME
main_app - Main logic of the application is declared here.

## FUNCTIONS

### `generate_form(str_editing, lst_columns, lst_values)`
Create a form with the columns and values passed as arguments so it can be rendered in a block
content on a template.

**Args:**

 * **`str_editing`**  Type of table to edit.
 * **`lst_columns`**  Columns of the table to be added into the form.
 * **`lst_values`**  Values of the table to be added into the form.

**Returns:** string with the form for the block content of the template.


### `handle_add_thing()`


### `handle_categories()`
Handles the categories creation and rendering on the page.

**Returns:** Flask template based on the request method.


### `handle_edit(str_to_edit, int_id)`
Edit records depending of the type of table is being requested.

**Args:**

str_to_edit:
int_id:

**Returns:** Flask template based on the request method.


### `handle_login()`
Handles the login page based on the request method, if request is POST it will check user
existence on the database. If the request is GET it will just send the login page.

**Returns:** Flask template based on the request method.


### `handle_logout()`
Remove the user sessionkey from database and remove email from the flask session.

**Returns:** It will redirect the user to home.


### `handle_register()`
Register the user on the db, if the request it type `GET` it will
return the form to be filled and then send it through a `POST`
request.

**Returns:** Flask template '_blank' modified based on the request.


### `handle_storage()`
Handles the storage creation and rendering on the page.

**Returns:** Flask template based on the request method.


### `handle_tags()`
Handles the showing or not of the tags on the system.

**Returns:** flask template.


### `handle_things()`
Handles the showing or not of the things belonging to the user.

**Returns:** flask template.


### `logs()`
This is to handle the requests of the application's logs.

**Returns:** flask.template with all logs of the application.


### `page_not_found(error)`
Function for handling all bad requests to the application.

**Args:**

error:

**Returns:** Template for 404 error code.


### `root()`
Main site where user goes to see available tools on the server and the description of them.

**Returns:** Template of the different tools of hosted.

## DATA
API = <flask_restful.Api object>
app = <Flask 'main_app'>
