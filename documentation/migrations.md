

```console
cd ./things_organizer
flask db upgrade
```


```console
flask db init
flask db migrate --rev-id <id-of-next-change> -m "change done on db"
flask db upgrade
```