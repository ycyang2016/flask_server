import datetime as dt
from settings.environment import app, db, error_helper
from flask                import request, jsonify, g
from flask.views          import MethodView
from flask_httpauth       import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from models.member        import Member
from sqlalchemy.exc       import IntegrityError
from sqlalchemy.orm.exc   import NoResultFound

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(account, passwd):
    try:
        member = db.session.query(Member).filter(Member.account==account).one()
        if member.verify_passwd(passwd):
            g.user = member
            return True
        return False
    except NoResultFound:
        return False

@basic_auth.error_handler
def account_error():
    return jsonify({
        'status': 'error.',
        'message': 'invalid account or password.'
    })  

@token_auth.verify_token
def verify_token(token):
    g.user = Member.verify_token(token)
    if g.user:
        return True
    else:
        return None

@token_auth.error_handler
def token_failed():
    return jsonify({
        'status': 'error.',
        'message': 'invalid token.'
    })

class Auth(MethodView):
    @multi_auth.login_required
    def get(self):
        api_result = {'status': 'success.'}
        return jsonify(api_result)

    @basic_auth.login_required
    def post(self):
        g.user.generate_token()
        api_result = {
            'status': 'success.',
            'token' : g.user.token,
            'deadline': (dt.datetime.now() + dt.timedelta(seconds=app.config['EXPIRATION'])).strftime('%Y-%m-%d %H:%M:%S'),
        }
        return jsonify(api_result)


auth_view = Auth.as_view('auth')