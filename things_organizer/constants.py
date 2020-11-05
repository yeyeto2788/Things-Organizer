import os

DATA_PATH = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    'data'
)
DB_PATH = os.path.abspath(os.path.join(DATA_PATH, 'db'))
REPORT_PATH = os.path.abspath(os.path.join(DATA_PATH, 'reports'))
LABEL_PATH = os.path.abspath(os.path.join(DATA_PATH, 'labels'))
