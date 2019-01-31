"""
DataBase Errors to be raised on the application do to problem on the DB.

"""


class DataBaseError(Exception):
    """
    Base Error for database operations, it will just raise a general exception with the message
    given as parameter.

    """
    def __init__(self, message, variable=None):
        super().__init__(message)
        self.message = message
        self.variable = variable

    def __str__(self):
        return self.message


class NotFoundError(DataBaseError):
    """
    DataBaseError used for records not found.

    """
    def __init__(self, variable=None):
        if variable is None:
            self.message = "No record(s) where found."
        else:
            self.message = "No record(s) called {} where found.".format(variable)
        self.variable = variable
        super().__init__(self.message, variable)

    def __str__(self):
        return self.message


class TableExistenceError(DataBaseError):
    """
    DataBaseError used for when a table do not exists on the database.

    If the `variable` is not message will be:
    `Table '<variable>' do not exists.`


    """
    def __init__(self, variable=None):
        if variable is None:
            self.message = "Table do not exists."
        else:
            self.message = "Table '{}' do not exists.".format(variable)
        self.variable = variable
        super().__init__(self.message, variable)

    def __str__(self):
        return self.message


class DataBaseExistenceError(DataBaseError):
    """
    DataBaseError used for when a database do not exists on a directory.

    If the `variable` is not message will be:
    `Database '<variable>' do not exists.`

    """
    def __init__(self, variable=None):
        if variable is None:
            self.message = "Database do not exists."
        else:
            self.message = "Database '{}' do not exists.".format(variable)
        self.variable = variable
        super().__init__(self.message, variable)

    def __str__(self):
        return self.message


class DataBaseConnectionError(DataBaseError):
    """
    DataBaseError used for when there is a database connection error.

    If the `variable` is not message will be:
    `Connecting to '<variable>' is not possible.`

    """
    def __init__(self, variable=None):
        if variable is None:
            self.message = "Connection error"
        else:
            self.message = "Connection error {}".format(variable)
        self.variable = variable
        super().__init__(self.message, variable)

    def __str__(self):
        return self.message


class AlreadyExistsError(DataBaseError):
    """
    DataBaseError used for when the data already exist on the database.

    If the `variable` is not message will be:
    `Connecting to '<variable>' is not possible.`

    """
    def __init__(self, variable=None):
        if variable is None:
            self.message = "Data already on the database."
        else:
            self.message = "Data already on the database.\nDue to {}".format(variable)
        self.variable = variable
        super().__init__(self.message, variable)

    def __str__(self):
        return self.message
