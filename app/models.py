from flask_login import UserMixin

from . import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(UserMixin, Base):
    __tablename__ = 'user'

    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    jobs = db.relationship('Job', backref='owner', lazy='dynamic')

    def __init__(self, name, email, password, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return '<User %r>' % self.name


job_status = ('WAITING', 'RUNNING', 'FINISHED', 'FAILED', 'STOPPED')


class Job(Base):
    __tablename__ = 'job'

    status = db.Column(db.Enum(*job_status, name='status'), default='WAITING')
    priority = db.Column(db.SmallInteger, default=0)
    total_time = db.Column(db.Integer, default=0)
    result_url = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id, priority=0):
        self.user_id = user_id
        self.priority = priority

    def __repr__(self):
        return '<Job %d>' % self.id

    def toJSON(self):
        return {'id': self.id, 'user_id': self.user_id,
                'status': self.status, 'priority': self.priority}

    def stop(self):
        pass

    def start(self):
        pass
