Flask_server
=============
A development environment of flask server, the server include password and token authorization.

Install
-------------
Install python
* Ubuntu
	```
	sudo apt-get update
	sudo apt-get install python2.7 python-pip
	```
* CentOS
	``` 
	sudo yum update
	```

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
```
git clone https://github.com/ycyang2016/flask_server
```

Quick start server
-------------
Before run this code, you have to make some preparation.

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
* \-\-port: server listen port number.
* \-\-threaded: server allow the number of thread run at the same time.
* \-\-process: server allow the number of process run at the same time.

How to use
-------------
Assume we create a python code named myapp.py in server folder, like this:
```
- flask_server/
	- models/
		- __init__.py
		- member.py
	- settings/
		- __init__.py
		- authentication.py
		- environment.py
	- __init__.py
	- run_server.py
	- myapp.py
```
* myapp.py
```python
from flask.views import MethodView 

def hello_func():
    return 'hello word, user.'
    
class HelloClass(MethodView):
    def get(self):
        return 'hello word, user.'

hello_class = HelloClass.as_view('hello')
```
### Non-authorization requirement case
In the case, you have to add some code at *line 6* in [run_server.py](https://github.com/ycyang2016/flask_server/blob/master/run_server.py).
```python
from myapp import hello_func, hello_class
app.add_url_rule('/hello/func' , func=hello_func , method=['GET'])
app.add_url_rule('/hello/class', func=hello_class, method=['GET'])
```
Then, you just run the server and link url http://your.server.ip:port/hello/func or http://your.server.ip:port/hello/class by your bowser. You can get the api result "hello word, user.".

### Authorization requirement case
In the case, when server receive a request, server will check ('account' and 'password') or 'token' in request header via [verify_password](https://github.com/ycyang2016/flask_server/blob/master/settings/authentication.py) (*line: 16*) or [verify_token](https://github.com/ycyang2016/flask_server/blob/master/settings/authentication.py) (*line: 34*). If you want to active the mechanism, you have to add the decorator(@basic_auth.login_required or @token_auth.login_required) at the head of your function.

First, modify myapp.py
```python
from flask.views import MethodView
from settings.authentication import basic_auth, token_auth, multi_auth

@token_auth.login_required
def hello_func():
    return 'hello word, user.'
    
class HelloClass(MethodView):
    @basic_auth.login_required
    def get(self):
        return 'hello word, user.'

hello_class = HelloClass.as_view('hello')
```
Second, you have to add some code at *line 6* in [run_server.py](https://github.com/ycyang2016/flask_server/blob/master/run_server.py).
```python
from myapp import hello_func, hello_class
app.add_url_rule('/hello/func' , func=hello_func , method=['GET'])
app.add_url_rule('/hello/class', func=hello_class, method=['GET'])
```
Then, you just run the server and link url http://your.server.ip:port/hello/class by your bowser. Server will make inquiries of you about account and password. If you input correct account and password, server will return 'hello word, user.'. Otherwise, server will reject the access.

If you want to test http://your.server.ip:port/hello/func, you must follow two step.
>Step 1. Use http://your.server.ip:port/auth to login server, and get token

>Step 2. you have to prepare api testing tool, like **Postman** or **Insomnia**. You have to choose **Bearer Token** in a tool and input correct token.

then, you will get the same result as http://your.server.ip:port/hello/class
