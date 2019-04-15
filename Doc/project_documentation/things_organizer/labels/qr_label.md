# qr_label.py


## NAME
qr_label - Module to generate QR labels with the data of a given Thing in the database.

## CLASSES
QRLabel

### `QRLabel(str_name, str_description, s_name, s_location)`

Class for generating the thing labels in QR code.

**Attributes:**
 * **`thing_name`**  Name to add on the label.
 * **`thing_description`**  Description to add on the label.
 * **`file_name`**  Name for the image generated.
 * **`file_directory`**  Directory where labels are stored.
 * **`storage_name`**  name of the storage.
 * **`storage_location`**  Location of the storage.

**Quick example:**
```python

label = QRLabel('SuperLabel', 'Sample description of a label')

label.generate_label()
```

Methods defined here:


### `__init__(self, str_name, str_description, s_name, s_location)`
Constructor method for the QRLabel object.

**Args:**

 * **`str_name`**  Name of the label
 * **`str_description`**  Description of the label.
 * **`s_name`**  Storage name.
 * **`s_location`**  Storage Location.


### `generate_label(self)`
Method to generate the label from class properties using the qr-code module.


Data descriptors defined here:

`__dict__`

dictionary for instance variables (if defined)

`__weakref__`

list of weak references to the object (if defined)
