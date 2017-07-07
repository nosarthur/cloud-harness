import datetime
from jose import jwt, JWTError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin

from . import db, login_manager


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(UserMixin, Base):
    __tablename__ = 'users'

    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    jobs = db.relationship('Job', backref='owner', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __init__(self, name, email, password, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return '<User %r id=%d>' % (self.name, self.id)

    @classmethod
    def validate(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user is None or not user.verify_password(password):
            raise ValueError('fail login')
        return user

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_token(self):
        """
        Generate authentication token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow()
                + datetime.timedelta(days=0, minutes=30),
                'iat': datetime.datetime.utcnow(),
                'iss': 'cloud-harness',
                'sub': str(self.id)
                }
            return jwt.encode(payload,
                              current_app.config['SECRET_KEY'],
                              algorithm='HS256')
        except:
            # FIXME: something needs to be done
            # raise
            return

    @staticmethod
    def decode_token(token):
        """
        @return user_id
        """
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])
            return int(payload['sub'])
        except JWTError:
            # raise
            return 0


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# maybe deprecate this func
@login_manager.request_loader
def load_user_from_request(request):
    """
    @param request: flask request object

    @return user instance or None
    """
    auth_str = request.headers.get('Authorization')
    token = auth_str.split(' ')[1] if auth_str else ''
    if token:
        user_id = User.decode_token(token)
        user = User.query.get(int(user_id))
        if user:
            return user
    return None


job_status = ('WAITING', 'RUNNING', 'FINISHED', 'FAILED', 'STOPPED')


class Job(Base):
    __tablename__ = 'job'

    status = db.Column(db.Enum(*job_status, name='status'), default='WAITING')
    priority = db.Column(db.SmallInteger, default=0)
    total_time = db.Column(db.Integer, default=0)
    result_url = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id, priority=0):
        self.user_id = user_id
        self.priority = priority

    def __repr__(self):
        return '<Job %d>' % self.id

    def stop(self):
        pass

    def start(self):
        pass
