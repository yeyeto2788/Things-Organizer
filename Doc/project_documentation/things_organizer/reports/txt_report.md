# txt_report.py


## NAME
txt_report - Report generator in `.txt` format in 3 different formats:

## DESCRIPTION
All items on database.

All items based on a category.

All items based on a storage.

Once report is generate it should return the directory of the file.

## CLASSES
`TXT`

### `TXT(file_name, int_user)`

`.txt` generator class to be use when creating reports.

Attributes:
 * **`file_directory`**  Directory where report will be saved.
 * **`file_name`**  Name to be used for the file.1
 * **`user_id`**  User id to query all things from that id.

Examples:
```python
from things_organizer.reports import TXT_Report


txt_report = TXT_Report('all_things', 1)

txt_report.get_all_things()

# Change name of the file for not overwriting it.

txt_report.file_name('all_by_category.txt', 2)

txt_report.get_by_category()

# Change name of the file for not overwriting it.

txt_report.file_name('all_by_storage.txt', 2)

txt_report.get_by_storage()

```

**Methods defined here:**


### `__init__(self, file_name, int_user)`
Constructor method for the TXT report generator.

**Args:**

 * **`file_name`**  Name for the `.txt` file.


### `get_all_things(self)`
Make a representation of the database to `.txt` file with all things in database.

**Returns:** Path of the file created.


### `get_by_category(self, int_id)`
Make a representation of the database to `.txt` file with all things in database filtered
by category.

**Args:**

 * **`int_id`**  ID of the category to filter by.

**Returns:** Path of the file created.


### `get_by_storage(self, int_id)`
Make a representation of the database to `.txt` file with all things in database filtered
by storage.

**Args:**

 * **`int_id`**  ID of the storage to filter by.

**Returns:** Path of the file created.


### `write_file(self, lst_columns, things, str_title)`
Common method for writing data into the `.txt` file.

**Args:**

 * **`lst_columns`**  Name of the columns of the file.
 * **`things`**  Dictionary with the things to be stored.
 * **`str_title`**  Title to be written on the `.txt` file.


Data descriptors defined here:

`__dict__`

dictionary for instance variables (if defined)

`__weakref__`

list of weak references to the object (if defined)
