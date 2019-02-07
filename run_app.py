import os

from things_organizer.main_app import app
from things_organizer.data_management.user import delete_all_sessions
from things_organizer.data_management import common

from waitress import serve

# TODO: Put all application related configuration into a file.
config = {'ip': '127.0.0.1', 'port': 8080}

# Generate a new Key each time the app is run.
app.secret_key = os.urandom(16)

# Comment the code below if you want to
# delete sessions every time the server starts
if common.exists_database():
    try:
        delete_all_sessions()
    except Exception as excerror:
        pass
else:
    common.create_tables()

# Run the server.
# If you want a debugging server set
# variable below to True, otherwise leave
# as it is.
DEBUG = True

if DEBUG:
    app.run(host=config['ip'], port=config['port'], threaded=True)
else:
    serve(app, listen='{}:{}'.format(config['ip'], config['port']))
