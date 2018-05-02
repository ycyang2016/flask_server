import re
import datetime as dt
from uuid                 import uuid1
from passlib.apps         import custom_app_context
from sqlalchemy           import Column, Integer, String, SmallInteger, Date, DateTime
from itsdangerous         import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from settings.environment import app, db

class Member(db.Model):
    __tablename__ = 'your table name'
    account      = Column('account'       , String(50), primary_key=True, nullable=False)
    passwd       = Column('passwd'        , String(128))
    secret_key   = Column('secret_key'    , String(50))
    token        = Column('token'         , String(256))
    #if you have other columns, you can write here

    def __init__(self, account, passwd, **args):
        self.account = account    
        self.secret_key  = uuid1()
        self.token       = None
        self.hash_password(passwd)
        #this function is column initialization

    def hash_password(self, passwd):
        self.passwd = custom_app_context.encrypt(passwd)

    def verify_passwd(self, passwd):
        return custom_app_context.verify(passwd, self.passwd)

    def generate_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in=app.config['EXPIRATION'])
        self.token = s.dumps({'account': self.account, 'secret_key': self.secret_key})
        db.session.commit()
        return self.token

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            member = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return Member.query.filter(Member.account==member['account'], Member.token==token).first()
        
