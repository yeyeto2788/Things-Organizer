# forms.py


## NAME
forms

## DESCRIPTION
Form definitions for rendering on the HTML pages and make easier the load and set of
items on the page.

## CLASSES

### `flask_wtf.form.FlaskForm(wtforms.form.Form)`
`CategoryForm`

`LoginForm`

`ReportForm`

`SignupForm`

`StorageForm`

`TagForm`

`ThingForm`

### `CategoryForm(*args, **kwargs)`

FlaskForm for adding a category.

**Methods defined here:**


### `validate_name(self, name_field)`
Validate that the category name does not exists on the database.

**Args:**

 * **`name_field`**  Name of the category to be checked.

**Returns:** True if name does not exists, else False.


**Data and other attributes defined here:**

`name`


### `LoginForm(*args, **kwargs)`

FlaskForm for login purposes.

**Data and other attributes defined here:**

`password` 

`remember_me` 

`username`

### `ReportForm(*args, **kwargs)`

FlaskForm for selecting the report to be printed.

**Data and other attributes defined here:**

`category`

`data_type`

`report_type`

`storage`


### `SignupForm(*args, **kwargs)`

FlaskForm for registering/signup purposes.


**Methods defined here:**


### `validate_email(self, email_field)`
Check whether the user's email exists on the database.

**Args:**

 * **`email_field`**  email to be checked.

**Returns:** True if not found, else False.


### `validate_username(self, username_field)`
Check whether the username exists on the database.

**Args:**

 * **`username_field`**  username to be checked.

**Returns:** True if not found, else False.


**Data and other attributes defined here:**

`email`

`password`

`password2`

`username`


### `StorageForm(*args, **kwargs)`

FlaskForm for adding storage.

**Methods defined here:**


### `validate(self)`
Validation of the Storage form checking whether the storage name and location pair
already exists or not.

**Returns:** True if the pair does not exists, else False.


**Data and other attributes defined here:**

`location`

`name`


### `TagForm(*args, **kwargs)`

FlaskForm for adding tags.

**Data and other attributes defined here:**

`name`


### `ThingForm(*args, **kwargs)`

FlaskForm for adding things.

**Methods defined here:**


### `validate(self)`
Validation of the Things form checking for tags separated by comma.

**Returns:** True if the form is validated by it parent, else False.


**Data and other attributes defined here:**

`category`

`description`

`name`

`quantity`

`storage`

`tags`

`unit`
