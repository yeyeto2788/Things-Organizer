
from things_organizer import app, DB

from waitress import serve

# TODO: Put all application related configuration into a file.
config = {'ip': '0.0.0.0', 'port': 8080}

# Generate a new Key each time the app is run.
app.secret_key = '3ZX\xb336\x15\x82/\xd5N1O\n\x9f\x8a'  # os.urandom(16)

# Create databases
DB.create_all()

# Run the server.
# If you want a debugging server set
# variable below to True, otherwise leave
# as it is.
DEBUG = True

if DEBUG:
    app.run(host=config['ip'], port=config['port'], threaded=True, debug=True)
else:
    serve(app, listen='{}:{}'.format(config['ip'], config['port']))
