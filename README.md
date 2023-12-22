# backend-data-handling-python

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

db-python  | 2023-12-21 15:27:36.787 UTC [58] ERROR:  column djangoapp_user.password does not exist at character 82
db-python  | 2023-12-21 15:27:36.787 UTC [58] STATEMENT:  SELECT "djangoapp_user"."id", "djangoapp_user"."name", "djangoapp_user"."email", "djangoapp_user"."password" FROM "djangoapp_user" LIMIT 21
djangoapp  | Internal Server Error: /users/
djangoapp  | Traceback (most recent call last):
djangoapp  |   File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
djangoapp  |     return self.cursor.execute(sql, params)
djangoapp  | psycopg2.errors.UndefinedColumn: column djangoapp_user.password does not exist
djangoapp  | LINE 1: ...djangoapp_user"."name", "djangoapp_user"."email", "djangoapp...

docker ps

docker exec -it db-python psql -U postgres -d postgres-python

\dt

SELECT * FROM djangoapp_user;

 id | name |  email   
----+------+----------
  1 | aaa  | aaa@mail
  3 | ccc  | ccc@mail


class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=250, unique=True)
    # password = models.CharField(max_length=14, null=True, blank=True)

djangoproject % python manage.py makemigrations
Migrations for 'djangoapp':
  djangoapp/migrations/0001_initial.py
    - Create model User

class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=14, null=True, blank=True)

djangoproject % python manage.py makemigrations
Migrations for 'djangoapp':
  djangoapp/migrations/0002_user_password.py
    - Add field password to user

docker-compose up --build

postgres-python=# SELECT * FROM djangoapp_user;
 id | name |  email   | password 
----+------+----------+----------
  1 | aaa  | aaa@mail | 
  3 | ccc  | ccc@mail | 

  OK
