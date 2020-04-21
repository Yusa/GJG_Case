## Good Job Games Backend Case


### Steps to Follow

#### Installation of Postgresql

##### Ubuntu:

```
$ sudo apt-get install postgresql postgresql-contrib

```

##### Fedora:

```
$ sudo yum install postgresql93-server
```

##### Arch Linux:

```
$ sudo pacman -S postgresql
$ sudo -iu postgres
[postgres]$ initdb -D /var/lib/postgres/data
[postgres]$ exit
$ sudo systemctl enable postgresql.service
$ sudo systemctl start postgresql.service

```

Now it is running on localhost and port:5432

I used Arch Linux as my development environment. Thus, other distros may need additional procedures as in Arch Linux after installation.

Then we should create a user:

```
$ sudo -iu postgres
[postgres]$ createuser --interactive -P  #You be prompted to enter username and password
[postgres@ebp ~]$ createdb scoreboard_db
exit
```



#### Installation of required Libraries for Project

Creating virtual environment is suggested but not necessary. You may skip to installing libraries.
```
$ virtualenv --python=python3 venv-GJG
$ source ./venv-GJG/bin/activate
```

Clone the project:
```
$ git clone https://github.com/Yusa/GJG_Case.git
$ cd GJG_Case
```

Installing libraries:
```
$ pip install -r requirements.txt
```

If you are not using virtual environment, you may need to run the command above with **sudo** privileges.


#### Settings and Run

You need to edit the database section of **settings.py** according to your database configurations you determined in PostgreSQL section. The values you need to edit are: **NAME**, **USER** and **PASSWORD**.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DATABASE_NAME',
        'USER': 'USER_NAME',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```

Make Migrations:
```
$ python manage.py migrate
```


Run the server:

```
$ python manage.py runserver
```


#### Resetting Database

To remove the tables in the database:

```
$ python manage.py migrate scoreboard_api zero
$ python manage.py migrate scoreboard_api
```

