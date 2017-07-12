import datetime
from jose import jwt, JWTError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects import postgresql
from flask import current_app

from . import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Worker(Base):
    __tablename__ = 'workers'

    ip = db.Column(postgresql.INET, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    job_id = db.Column(db.Integer)
    date_finished = db.Column(db.DateTime)

    def __init__(self, ip, price):
        self.ip = ip
        self.price = price

    def check_health(self):
        # current_timestamp - date_modified > some time
        if 0:
            self.data_finished = db.func.current_timestamp()
            job = Job.query.get(self.job_id)
            job.status = 'FAILED'


class User(Base):
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


job_status = ('WAITING', 'RUNNING', 'FINISHED', 'FAILED', 'STOPPED')


class Job(Base):
    __tablename__ = 'jobs'

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
