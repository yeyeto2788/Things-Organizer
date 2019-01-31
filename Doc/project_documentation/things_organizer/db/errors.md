# errors.py

## NAME
errors - DataBase Errors to be raised on the application do to problem on the DB.

## CLASSES

### `builtins.Exception(builtins.BaseException)`
DataBaseError
AlreadyExistsError
DataBaseConnectionError
DataBaseExistenceError
NotFoundError
TableExistenceError


### `class AlreadyExistsError(DataBaseError)`
DataBaseError used for when the data already exist on the database.

If the `variable` is not message will be:
`Connecting to '<variable>' is not possible.`

Method resolution order:
AlreadyExistsError
DataBaseError
builtins.Exception
builtins.BaseException
builtins.object

Methods defined here:


### `__init__(self, variable=None)`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `__str__(self)`

### `Return str(self).`


Data descriptors inherited from DataBaseError:

__weakref__
list of weak references to the object (if defined)


Methods inherited from builtins.Exception:


### `__new__(*args, **kwargs) from builtins.type`

### `Create and return a new object.  See help(type) for accurate signature.`


Methods inherited from builtins.BaseException:


### `__delattr__(self, name, /)`

### `Implement delattr(self, name).`


### `__getattribute__(self, name, /)`

### `Return getattr(self, name).`


### `__reduce__(...)`
helper for pickle


### `__repr__(self, /)`

### `Return repr(self).`


### `__setattr__(self, name, value, /)`

### `Implement setattr(self, name, value).`


### `__setstate__(...)`


### `with_traceback(...)`

### `Exception.with_traceback(tb) --`
set self.__traceback__ to tb and return self.


Data descriptors inherited from builtins.BaseException:

__cause__
exception cause

__context__
exception context

__dict__

__suppress_context__

__traceback__

args


### `class DataBaseConnectionError(DataBaseError)`
DataBaseError used for when there is a database connection error.

If the `variable` is not message will be:
`Connecting to '<variable>' is not possible.`

Method resolution order:
DataBaseConnectionError
DataBaseError
builtins.Exception
builtins.BaseException
builtins.object

Methods defined here:


### `__init__(self, variable=None)`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `__str__(self)`

### `Return str(self).`


Data descriptors inherited from DataBaseError:

__weakref__
list of weak references to the object (if defined)


Methods inherited from builtins.Exception:


### `__new__(*args, **kwargs) from builtins.type`

### `Create and return a new object.  See help(type) for accurate signature.`


Methods inherited from builtins.BaseException:


### `__delattr__(self, name, /)`

### `Implement delattr(self, name).`


### `__getattribute__(self, name, /)`

### `Return getattr(self, name).`


### `__reduce__(...)`
helper for pickle


### `__repr__(self, /)`

### `Return repr(self).`


### `__setattr__(self, name, value, /)`

### `Implement setattr(self, name, value).`


### `__setstate__(...)`


### `with_traceback(...)`

### `Exception.with_traceback(tb) --`
set self.__traceback__ to tb and return self.


Data descriptors inherited from builtins.BaseException:

__cause__
exception cause

__context__
exception context

__dict__

__suppress_context__

__traceback__

args


### `class DataBaseError(builtins.Exception)`
Base Error for database operations, it will just raise a general exception with the message
given as parameter.

Method resolution order:
DataBaseError
builtins.Exception
builtins.BaseException
builtins.object

Methods defined here:


### `__init__(self, message, variable=None)`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `__str__(self)`

### `Return str(self).`


Data descriptors defined here:

__weakref__
list of weak references to the object (if defined)


Methods inherited from builtins.Exception:


### `__new__(*args, **kwargs) from builtins.type`

### `Create and return a new object.  See help(type) for accurate signature.`


Methods inherited from builtins.BaseException:


### `__delattr__(self, name, /)`

### `Implement delattr(self, name).`


### `__getattribute__(self, name, /)`

### `Return getattr(self, name).`


### `__reduce__(...)`
helper for pickle


### `__repr__(self, /)`

### `Return repr(self).`


### `__setattr__(self, name, value, /)`

### `Implement setattr(self, name, value).`


### `__setstate__(...)`


### `with_traceback(...)`

### `Exception.with_traceback(tb) --`
set self.__traceback__ to tb and return self.


Data descriptors inherited from builtins.BaseException:

__cause__
exception cause

__context__
exception context

__dict__

__suppress_context__

__traceback__

args


### `class DataBaseExistenceError(DataBaseError)`
DataBaseError used for when a database do not exists on a directory.

If the `variable` is not message will be:
`Database '<variable>' do not exists.`

Method resolution order:
DataBaseExistenceError
DataBaseError
builtins.Exception
builtins.BaseException
builtins.object

Methods defined here:


### `__init__(self, variable=None)`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `__str__(self)`

### `Return str(self).`


Data descriptors inherited from DataBaseError:

__weakref__
list of weak references to the object (if defined)


Methods inherited from builtins.Exception:


### `__new__(*args, **kwargs) from builtins.type`

### `Create and return a new object.  See help(type) for accurate signature.`


Methods inherited from builtins.BaseException:


### `__delattr__(self, name, /)`

### `Implement delattr(self, name).`


### `__getattribute__(self, name, /)`

### `Return getattr(self, name).`


### `__reduce__(...)`
helper for pickle


### `__repr__(self, /)`

### `Return repr(self).`


### `__setattr__(self, name, value, /)`

### `Implement setattr(self, name, value).`


### `__setstate__(...)`


### `with_traceback(...)`

### `Exception.with_traceback(tb) --`
set self.__traceback__ to tb and return self.


Data descriptors inherited from builtins.BaseException:

__cause__
exception cause

__context__
exception context

__dict__

__suppress_context__

__traceback__

args


### `class NotFoundError(DataBaseError)`
DataBaseError used for records not found.

Method resolution order:
NotFoundError
DataBaseError
builtins.Exception
builtins.BaseException
builtins.object

Methods defined here:


### `__init__(self, variable=None)`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `__str__(self)`

### `Return str(self).`


Data descriptors inherited from DataBaseError:

__weakref__
list of weak references to the object (if defined)


Methods inherited from builtins.Exception:


### `__new__(*args, **kwargs) from builtins.type`

### `Create and return a new object.  See help(type) for accurate signature.`


Methods inherited from builtins.BaseException:


### `__delattr__(self, name, /)`

### `Implement delattr(self, name).`


### `__getattribute__(self, name, /)`

### `Return getattr(self, name).`


### `__reduce__(...)`
helper for pickle


### `__repr__(self, /)`

### `Return repr(self).`


### `__setattr__(self, name, value, /)`

### `Implement setattr(self, name, value).`


### `__setstate__(...)`


### `with_traceback(...)`

### `Exception.with_traceback(tb) --`
set self.__traceback__ to tb and return self.


Data descriptors inherited from builtins.BaseException:

__cause__
exception cause

__context__
exception context

__dict__

__suppress_context__

__traceback__

args


### `class TableExistenceError(DataBaseError)`
DataBaseError used for when a table do not exists on the database.

If the `variable` is not message will be:
`Table '<variable>' do not exists.`

Method resolution order:
TableExistenceError
DataBaseError
builtins.Exception
builtins.BaseException
builtins.object

Methods defined here:


### `__init__(self, variable=None)`

### `Initialize self.  See help(type(self)) for accurate signature.`


### `__str__(self)`

### `Return str(self).`


Data descriptors inherited from DataBaseError:

__weakref__
list of weak references to the object (if defined)


Methods inherited from builtins.Exception:


### `__new__(*args, **kwargs) from builtins.type`

### `Create and return a new object.  See help(type) for accurate signature.`


Methods inherited from builtins.BaseException:


### `__delattr__(self, name, /)`

### `Implement delattr(self, name).`


### `__getattribute__(self, name, /)`

### `Return getattr(self, name).`


### `__reduce__(...)`
helper for pickle


### `__repr__(self, /)`

### `Return repr(self).`


### `__setattr__(self, name, value, /)`

### `Implement setattr(self, name, value).`


### `__setstate__(...)`


### `with_traceback(...)`

### `Exception.with_traceback(tb) --`
set self.__traceback__ to tb and return self.


Data descriptors inherited from builtins.BaseException:

__cause__
exception cause

__context__
exception context

__dict__

__suppress_context__

__traceback__

args
