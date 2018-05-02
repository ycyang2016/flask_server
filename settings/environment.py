import sys
from flask            import Flask
from flask_wtf.csrf   import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from itertools        import izip


csrf = CSRFProtect()

class Config(object):
    #standard flask configuration
    DEBUG      = False
    TESTING    = False
    SECRET_KEY = 'your secret key'
    #flask-sqlalchmy extension configuration
    SQLALCHEMY_DATABASE_URI        = 'your database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #token expiration time
    EXPIRATION = 1800


class Development(Config):
    #standard flask configuration
    DEBUG            = True
    #flask-wtf extension configuration
    WTF_CSRF_ENABLED    = False
    WTF_CSRF_SSL_STRICT = False
    #flask-sqlalchmy extension configuration
    SQLALCHEMY_ECHO                = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #unlimit token expiration time
    EXPIRATION = 28800 # 8 hours

class Production(Config):
    SQLALCHEMY_DATABASE_URI        = 'your database'


def read_command(version, *command):
    runtime_settings = {
        'host': '0.0.0.0',
        'port': 5000,
        'threaded': None,
        'processes': None
    }

    for arg_name, arg_value in izip(*[iter(command)] * 2):
        if arg_name.startswith('--') and arg_name[2:] in runtime_settings:
            runtime_settings[arg_name[2:]] = int(arg_value)

    runtime_settings['use_reloader'] = (version != 'Production')
    return runtime_settings


def error_helper(message):
    if len(re.compile(r'\(1062, \"Duplicate entry \'.+\' for key \'PRIMARY\'\"\)').findall(message)):
        return 'account already exists.'
    print message
    return 'internal server error'


APP_VERSION  = sys.argv[1]
RUN_SETTING = read_command(APP_VERSION, *tuple(sys.argv[2:]))

app = Flask(__name__)
app.config.from_object('settings.environment.%s' % APP_VERSION)
csrf.init_app(app)
db  = SQLAlchemy(app)
