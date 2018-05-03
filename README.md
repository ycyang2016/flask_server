Flask_server
=============
A development environment of flask server, the server include password and token authorization

Install
-------------
Install python
* Ubuntu
	```
	sudo apt-get update
	sudo apt-get install python2.7 python-pip
	```
* CentOS
		`` sudo yum update``

Install python package
```
sudo pip install --upgrade pip
sudo pip install -y
	flask \
	flask_wtf \
	Flask-SQLAlchemy \
	flask_httpauth \
	passlib \
	itsdangerous
```
Install the flask server
``git clone https://github.com/ycyang2016/flask_server``

Quick start server
-------------
Before run this code, you have to make some preparation 

### Database
>you have to create a database and table in mysql server.
#### table schema
|Column name|Column type |Column attribute|
|:----------|:----------:|:--------------:|
|account    |VARCHAR(50) |  primary_key   |
|passwd     |VARCHAR(128)|    not null    |
|secret_key |VARCHAR(50) |    not null    |
|token      |VARCHAR(256)|                |


### Code settings
you have to modify some code:
1. Server **secret key**. The key is in the  [settings/environment.py](https://github.com/ycyang2016/flask_server/tree/master/settings/environment.py) : *line 14*.
2. Server account **database URI**. The uri is in the [settings/environment.py](https://github.com/ycyang2016/flask_server/tree/master/settings/environment.py) : *line 16* and *35*.
3. Server account **mysql table name**. The table name in the [models/member.py](https://github.com/ycyang2016/flask_server/blob/master/models/member.py) : *line 10*.
### Run server
python run_server.py <Development|Production> [--port|--threaded|--process]
> python run_server.py Development --port 12345

* <>: This is config settings. The file in [settings/environment.py](https://github.com/ycyang2016/flask_server/tree/master/settings/environment.py). Development means use the Development class.
* \-\-port: server listen port number
* \-\-threaded: server allow the number of thread run at the same time
* \-\-process: server allow the number of process run at the same time

