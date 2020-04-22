## Good Job Games Backend Case


### Steps to Follow

Project is written with Python3. If it is not installed, install Python3 first.

#### Installation of Postgresql

##### Ubuntu:

```
$ sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-all

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

The project is deployed on GPC server which has Ubuntu as OS, I also tested the instructions for Ubuntu and works fine. The IP and the port of the machine is:


**http://35.214.117.221:8000/**


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
$ python manage.py runserver 0.0.0.0:8000
```


#### Resetting Database

To remove the tables in the database:

```
$ python manage.py migrate scoreboard_api zero
$ python manage.py migrate scoreboard_api
```


#### Populating Data for the Database

I also wrote a small script for filling the database. It generates random Name - Surname, point, GUID and with using /user/create/bulk/ endpoint which is a specific endpoint for bulk user creation, inserts them to database. 

To run the script, first libraries must be installed as follows.

```
$ pip install requirements-populator.txt
```

Then the script can be edited to adjust amoun of users to be created and how many of them should be inserted in each request. **COUNT** variable is the amount of users to insert, **EACH** variable is the amount to insert at each request.

```
$ python db_populater.py
```

#### Tests

There are unit tests for each view and tests can be run with the following command:

```
$ python manage.py test
```

#### Endpoints

Each endpoint is listed below.

##### 1 - user/create/

Takes JSON data such. Example query in python:

```
import requests, json

url = "http://35.214.117.221/user/create/"
headers = {'Content-type': 'application/json'}
user = {
	"display_name":"Friedrich",
	"rank":2,
	"points":1930,
	"user_id":"63afa900-c978-43fa-8d6b-9f79aa9b0aee",
	"country":"DE"
}

r = requests.post(uri, data=json.dumps(user), headers=headers)
print(r.json())

```
Server will respond either the following with **200** status code:
```
{"result":"1"}
```
or error message with **400** status code such as:
```
{"error": "User already exists."}
```


##### 2 - user/profile/

Takes the Globally Unique Identifier which is user id and returns the details of this user. 

```
import requests
url = "http://35.214.117.221:8000/user/profile/"
uid = "ed7015c9-a8f8-405c-a296-14f3ca432b78"

r = requests.get(f"{url}{uid}")
print(r.json())

```
The result will be in the following format with **200** status code:
```
{
    "display_name": "Mark Kinzer",
    "points": 999997730,
    "rank": 899,
    "user_id": "ed7015c9-a8f8-405c-a296-14f3ca432b78"
}
```
or in case of errors with the **400** bad request status code:

```
{
	"error": "User ID is not given in the correct format."
}
```
```
{
	"error": "User doesn't exist"
}
```

##### 3 - leaderboard/

Returns the global leaderboard ordered by the ranks with pagination.

```
import requests
url = "http://35.214.117.221:8000/leaderboard/"

r = requests.get(url)
print(r.json())
```

Result will be in the following format with **200** status code:
```
{
    'count': 900,
    'next': 'http://35.214.117.221:8000/leaderboard/?page=2',
    'previous': None,
    'results': [
    {
        'display_name': 'Ann Tetreault',
        'points': 999999997,
        'rank': 1,
        'country': 'id'
    },
    {
        'display_name': 'Rachel Oelze',
        'points': 999999997,
        'rank': 2,
        'country': 'gr'
    },
    {
        'display_name': 'Cari Herzberg',
        'points': 999999992,
        'rank': 3,
        'country': 'mo'
    },
    
    .
    .
    .
    .
    
    {
        'display_name': 'Jim Noe',
        'points': 999999949,
        'rank': 19,
        'country': 'hm'
    },
    {
        'display_name': 'Alicia Chong',
        'points': 999999949,
        'rank': 20,
        'country': 'vu'
    }]
}
```
Errors will be in the following format with **400** Bad Request status code:

```
{
	"error": "Page number is not valid."
}
```

##### 4 - leaderboard/<country_code>/

Returns the leaderboard with filtering the country and ordered by the ranks with pagination.

```
import requests
url = "http://35.214.117.221:8000/leaderboard/tr"

r = requests.get(url)
print(r.json())
```

Result will be in the following format with **200** status code:

```
{
    'count': 5,
    'next': None,
    'previous': None,
    'results': [
    {
        'display_name': 'Greg Crawford',
        'points': 999999851,
        'rank': 61,
        'country': 'cu'
    },
    {
        'display_name': 'Georgette Robinson',
        'points': 999999563,
        'rank': 176,
        'country': 'cu'
    },
    {
        'display_name': 'Virginia White',
        'points': 999999186,
        'rank': 323,
        'country': 'cu'
    },
    {
        'display_name': 'James Martinez',
        'points': 999999071,
        'rank': 365,
        'country': 'cu'
    },
    {
        'display_name': 'Harold Reed',
        'points': 999998517,
        'rank': 588,
        'country': 'cu'
    }]
}
```
Errors will be in the following format with **400** Bad Request status code:

```
{
	"error": "Country code is not valid."
}
```

##### 5 - score/submit/

From this endpoint, individual user score is submitted.

```
import requests, json

url = "http://35.214.117.221/score/submit/"
headers = {'Content-type': 'application/json'}
user_score = {
	"score_worth":100000,
	"user_id":"ed7015c9-a8f8-405c-a296-14f3ca432b78",
	"timestamp":1231412351
}

r = requests.post(uri, data=json.dumps(user_score), headers=headers)
print(r.json())
```
Result will be in the following format with **200** status code:

```
{
	"result":"1"
}
```
Errors will be in the following format with **400** Bad Request status code:

```
{
	"error": "user_id is not given."
}
```
```
{
	"error":"User with given user_id does not exists."
}
```

##### 6 - user/create/bulk/

This endpoint is designed to create multiple users with a single query:
```
import requests, json

url = "http://35.214.117.221:8000/user/create/bulk/"
headers = {'Content-type': 'application/json'}
users = {'count': 5,
    	'users': [   
	    			 {   'country': 'us',
	                     'display_name': 'Margaret Cox',
	                     'points': 999999996,
	                     'rank': 1,
	                     'user_id': '2fbf0a61-023c-42f9-8d34-553b09b8412f'},
	                 {   'country': 'at',
	                     'display_name': 'Kevin Oneal',
	                     'points': 999999991,
	                     'rank': 2,
	                     'user_id': '5d673525-956a-488e-8299-a022314cde60'},
	                 {   'country': 'ru',
	                     'display_name': 'Yolanda Jamon',
	                     'points': 999999991,
	                     'rank': 3,
	                     'user_id': '1b2c9ad6-3c9c-4b3e-aaa2-2a4c0cfd092a'},
	                 {   'country': 'ly',
	                     'display_name': 'Joyce Keogh',
	                     'points': 999999987,
	                     'rank': 4,
	                     'user_id': '796c56fa-4989-4df7-8e2b-487ca9eb91d9'},
	                 {   'country': 'cy',
	                     'display_name': 'Lily Huggins',
	                     'points': 999999986,
	                     'rank': 5,
	                     'user_id': 'a0fee6b5-d4fd-4edc-973e-3ef4cc73f33d'}
                 ]
         }


r = requests.post(url, data=json.dumps(users), headers=headers)
print(r.json())
```

Result will be with 200 status code and if no error it will be as follows:

```
[]
```
if there is an error with creating users, each error about each user will be in the response as follows:

```
[
{
    'error': 'User already exists.',
    'user':
    {
        'country': 'us',
        'display_name': 'Margaret Cox',
        'points': 999999996,
        'rank': 1,
        'user_id': '2fbf0a61-023c-42f9-8d34-553b09b8412f'
    }
},
{
    'error': 'User already exists.',
    'user':
    {
        'country': 'at',
        'display_name': 'Kevin Oneal',
        'points': 999999991,
        'rank': 2,
        'user_id': '5d673525-956a-488e-8299-a022314cde60'
    }
},
{
    'error': 'User already exists.',
    'user':
    {
        'country': 'ru',
        'display_name': 'Yolanda Jamon',
        'points': 999999991,
        'rank': 3,
        'user_id': '1b2c9ad6-3c9c-4b3e-aaa2-2a4c0cfd092a'
    }
},
{
    'error': 'User already exists.',
    'user':
    {
        'country': 'ly',
        'display_name': 'Joyce Keogh',
        'points': 999999987,
        'rank': 4,
        'user_id': '796c56fa-4989-4df7-8e2b-487ca9eb91d9'
    }
},
{
    'error': 'User already exists.',
    'user':
    {
        'country': 'cy',
        'display_name': 'Lily Huggins',
        'points': 999999986,
        'rank': 5,
        'user_id': 'a0fee6b5-d4fd-4edc-973e-3ef4cc73f33d'
    }
}]
```

Other errors will be returned with 400 status code and in the following format:

```
{
	"error": "count-amount mismatch."
}
```
```
{
	"error": "count is not specified."
}
```