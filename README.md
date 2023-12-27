# backend-data-handling-python

```
brew install python@3.10

virtualenv -p python3.10 venv

source venv/bin/activate

deactivate

pip install django-admin-cli

pip install django

django-admin startproject djangoproject

pip freeze >requirements.txt

pip install -r requirements.txt

chmod +x django.sh

docker-compose up -d db-python

docker ps -a

docker compose logs

docker-compose down -v

docker compose build

docker compose up

docker exec -it djangoapp /bin/bash

python manage.py makemigrations

python manage.py migrate

exit

docker restart djangoapp

db-python | 2023-12-21 15:27:36.787 UTC [58] ERROR: column djangoapp_user.password does not exist at character 82
db-python | 2023-12-21 15:27:36.787 UTC [58] STATEMENT: SELECT "djangoapp_user"."id", "djangoapp_user"."name", "djangoapp_user"."email", "djangoapp_user"."password" FROM "djangoapp_user" LIMIT 21
djangoapp | Internal Server Error: /users/
djangoapp | Traceback (most recent call last):
djangoapp | File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in \_execute
djangoapp | return self.cursor.execute(sql, params)
djangoapp | psycopg2.errors.UndefinedColumn: column djangoapp_user.password does not exist
djangoapp | LINE 1: ...djangoapp_user"."name", "djangoapp_user"."email", "djangoapp...

docker ps

docker exec -it db-python psql -U postgres -d postgres-python

\dt

SELECT \* FROM djangoapp_user;

id | name | email
----+------+----------
1 | aaa | aaa@mail
3 | ccc | ccc@mail

class User(models.Model):
name = models.CharField(max_length=50, unique=True)
email = models.CharField(max_length=250, unique=True) # password = models.CharField(max_length=14, null=True, blank=True)

djangoproject % python manage.py makemigrations
Migrations for 'djangoapp':
djangoapp/migrations/0001_initial.py - Create model User

class User(models.Model):
name = models.CharField(max_length=50, unique=True)
email = models.CharField(max_length=250, unique=True)
password = models.CharField(max_length=14, null=True, blank=True)

djangoproject % python manage.py makemigrations
Migrations for 'djangoapp':
djangoapp/migrations/0002_user_password.py - Add field password to user

docker-compose up --build

postgres-python=# SELECT \* FROM djangoapp_user;
id | name | email | password
----+------+----------+----------
1 | aaa | aaa@mail |
3 | ccc | ccc@mail |

psycopg2.errors.DuplicateColumn: column "password" of relation "djangoapp_user" already exists

delete all migrations

python manage.py makemigrations

python manage.py migrate

docker compose up --build

curl \
 -X POST \
 -H "Content-Type: application/json" \
 -d '{"username": "a21", "password": "Aa2345678$"}' \
 localhost:8000/token/

curl -X POST -H "Content-Type: application/json" -d '{"username": "a21", "password": "Aa2345678$"}' localhost:8000/token/

python manage.py createsuperuser

Username: admin
Email address: admin@example.com
Password:123456

curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "123456"}' localhost:8000/token/

{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMzU1MDU0OCwiaWF0IjoxNzAzNDY0MTQ4LCJqdGkiOiJhNzEyM2Q4MWNhN2Q0ZjE2OTYwNDRkOGFiNDQzNGViNCIsInVzZXJfaWQiOjF9.WDR0UshL-igasuqtnmKyLFYjocUoofBONGy1r5qpYs0","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzNDY3NzQ4LCJpYXQiOjE3MDM0NjQxNDgsImp0aSI6IjJlY2ViYWJiZjk2OTRmMTJiOTlmNzljNGU1ZGY1ZjA3IiwidXNlcl9pZCI6MX0.qC3K4t78OxHPq78HTjOsKj-JUgFBsT4Qk2IGlcOQgdo"}%

curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzNDcyNzU1LCJpYXQiOjE3MDM0NjkxNTUsImp0aSI6IjQ5MDIwM2JkYmViZjQwNzI5Mzk2Y2FhODE0MDMyZjZjIiwidXNlcl9pZCI6MX0.MVFtudX3XKjwksDgHd95ZRHIvPsVeHjaiDjXFsGJJ94" localhost:8000/users/

[{"uuid":"387b3acd-f712-43f7-89cc-9936726a74cf","name":"a21","email":"a23@mail.com","password":"Aa2345678$"}]%


pip freeze > requirements.txt


python manage.py migrate djangoapp zero
python manage.py makemigrations
python manage.py migrate

docker ps -a

docker compose up --build
docker exec -it djangoapp /bin/bash

docker exec -it db-python psql -U postgres -d postgres-python

\dt

SELECT \* FROM djangoapp_user;




docker ps -a

docker exec -it db-python psql -U postgres -d postgres

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'postgres-python' AND pid <> pg_backend_pid();

DROP DATABASE "postgres-python";
CREATE DATABASE "postgres-python";

docker exec -it djangoapp /bin/bash

python manage.py makemigrations
python manage.py migrate

docker compose up --build

```
