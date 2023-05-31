## Migration Flow for Model Field Changes:

After Each model field change
~~~bash
python manage.py makemigrations
python manage.py migrate
~~~

commands must be executed for the changes to take effect.

You can find out if a migration is required by executing makemigrations. If a new file is created by makemigrations, migrate command must be called as well.

-------------------