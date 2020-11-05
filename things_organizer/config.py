import os
import sys

import things_organizer.constants

SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(16)

DATABASE_PATH = os.path.abspath(
    os.path.join(things_organizer.constants.DB_PATH, "things_organizer.db")
)

if sys.platform == 'linux':
    SQLALCHEMY_DATABASE_URI = "sqlite:////{}".format(DATABASE_PATH)
    print(f"Using the db {DATABASE_PATH}")

else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DATABASE_PATH)
    print(f"Using the db {DATABASE_PATH}")
