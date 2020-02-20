# Migrations

## First time setup
```console
cd ./things_organizer
flask db upgrade
```

## Making a new migration
In case you want to make changes on the database schema, once those changes are applied in the code 
we need to make the new migration so all changes in code are reflected on the database and 
anyone using it have those changes.
```console
flask db migrate --rev-id <id-of-next-change> -m "change done on db"
flask db upgrade
```