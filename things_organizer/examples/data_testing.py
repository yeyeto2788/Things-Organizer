import things_organizer.data_management.common
from things_organizer import data_management
from things_organizer.db import operations

print("\nGet data from table that does NOT exists")
bln_result = things_organizer.data_management.common.is_table_configured('testing.db', 'AGENTING')
print(bln_result)


print("\nGet data from table that exists and have data")
bln_result = things_organizer.data_management.common.is_table_configured('testing.db', 'AGENTS')
print(bln_result)

db = operations.DataBase('testing.db')
db.connect_to_db()

# Uncomment code below only once.
# db.create_table('USERS', ['id', 'name', 'lastname', 'age'])

print("\nGet data from table that exists and does NOT have data")
bln_result = things_organizer.data_management.common.is_table_configured('testing.db', 'USERS')
print(bln_result)


db_log = operations.DataBaseLogger()
db_log.log_error('First log added...')
