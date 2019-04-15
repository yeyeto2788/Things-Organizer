# storages.py


## NAME
storages - API end point for the things categories.

## CLASSES


### `class StoragesAPI(flask_restful.Resource)`
Class wrapper for the flask_restful.Resource in order to create the API.

**NOTE:** By now the only method allow is `GET`, probably more methods will be added.


**Static methods defined here:**

### `get(int_id=None)`
Find a storage for a given ID, if no ID is provided it will return all available
storage on table.

**Args:**

 * **`int_id`**  Id of the category to be searched.

**Returns:** Response from jsonify function of flask.


**Data and other attributes defined here:**

`methods`


**Data descriptors inherited from flask.views.View:**

`__dict__`

dictionary for instance variables (if defined)

`__weakref__`

list of weak references to the object (if defined)

