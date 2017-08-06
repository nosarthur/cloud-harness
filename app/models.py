import boto3
# import base64
import datetime
from jose import jwt, JWTError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from . import db
from views.home import BadRequestError


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow(),
                              onupdate=datetime.datetime.utcnow())


def dump_aws_instance(instance_id, on_demand=False):
    s = boto3.Session(profile_name='dev')
    ec2 = s.resource('ec2', region_name='us-east-1')
    try:
        ec2.Instance(instance_id).terminate()
    except Exception as e:
        raise BadRequestError('Cannot terminate AWS instance %s: %s.' %
                              (instance_id, e))


def get_aws_instances(n_workers=1, on_demand=False, price=None):
    """
    @type price: C{float}
    """
    with open('scripts/worker.sh') as f:
        startup = f.read()
        print(startup)
#        startup = base64.b64encode(startup.encode('ascii'))
    amz201703 = 'ami-0e297018'
    s = boto3.Session(profile_name='dev', region_name='us-east-1')
    if on_demand:
        ec2 = s.resource('ec2')
        rc = ec2.create_instances(ImageId=amz201703,
                                  InstanceType='t2.nano',
                                  MinCount=1,
                                  MaxCount=n_workers,
                                  UserData=startup,
                                  KeyName='harness',
                                  IamInstanceProfile={}
                                      # 'Name': 'harness-worker'},
                                  )
    else:  # spot instance
        client = s.client('ec2')
        rc = client.request_spot_instances(
                DryRun=False,
                SpotPrice=str(price),
                Type='one-time',
                LaunchSpecification={'ImageId': amz201703,
                                     'KeyName': 'harness',
                                     'InstanceType': 'm4.large',
                                     'UserData': startup,
                                     },
                InstanceCount=n_workers,
               )
    if not rc:
        raise BadRequestError('Cannot get AWS instance.')
    return rc


class Worker(Base):
    __tablename__ = 'workers'

    instance_id = db.Column(db.String, nullable=False)
    job_id = db.Column(db.Integer)
    date_finished = db.Column(db.DateTime)

    def __init__(self, instance_id, job_id=None):
        self.instance_id = instance_id
        self.job_id = job_id

    def stop(self):
        if self.date_finished:
            raise BadRequestError('Worker has already stopped.')
        dump_aws_instance(self.instance_id, on_demand=True)
        self.date_finished = datetime.datetime.utcnow()

    def checkHealth(self):
        # FIXME: make the return values more meaningful for debugging
        if not self.job_id:
            return False
        if (datetime.datetime.utcnow() - self.date_modified >
                datetime.timedelta(minutes=15)):
            self.date_finished = datetime.datetime.utcnow()
            job = Job.query.get(self.job_id)
            job.status = 'FAILED'
            return False
        return True


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

    def isOwner(self, job_id):
        if self.is_admin:
            return True
        ids = set(j.id for j in self.jobs)
        return job_id in ids

    def __repr__(self):
        return '<User %r id=%d>' % (self.name, self.id)

    @classmethod
    def validate(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user is None or not user.verifyPassword(password):
            raise BadRequestError('Login failed.')
        return user

    def verifyPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def encodeToken(self):
        """
        Generate authentication token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1),
                'iat': datetime.datetime.utcnow(),
                'iss': 'cloud-harness',
                'sub': str(self.id)
            }
            return jwt.encode(payload,
                              current_app.config['SECRET_KEY'],
                              algorithm='HS256')
        except Exception as e:
            raise BadRequestError('Cannot create JWT token: %s' % e)

    @staticmethod
    def decodeToken(token):
        """
        @return user_id
        """
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])
            return int(payload['sub'])
        except JWTError as e:
            raise BadRequestError('JWT error: %s' % e)


class JobState(object):
    """
    Base class for various job states.
    """
    def __init__(self, job):
        """
        @type job: L{Job} instance
        """
        self.job = job

    def goTo(self, status):
        raise BadRequestError('Cannot go to %s state.' % status)


class Finished(JobState):
    pass


class Stopped(JobState):
    pass


class Failed(JobState):
    pass


class Queued(JobState):
    def goTo(self, status):
        if status not in ('STOPPED', 'RUNNING', ):
            raise BadRequestError('Queued job cannot go to %s state.' % status)
        self.job.status = status


class Waiting(JobState):
    def goTo(self, status):
        if status != 'QUEUED':
            raise BadRequestError('Waiting job cannot go to %s state.' % status)
        self.job.status = 'QUEUED'


class Running(JobState):
    def goTo(self, status):
        if status not in ('STOPPED', 'FINISHED', 'FAILED'):
            raise BadRequestError('Job is not running.')
        self.job.status = status


job_status = ('WAITING', 'RUNNING', 'FINISHED', 'FAILED', 'STOPPED', 'QUEUED')
JOB_STATUS_MAP = dict(zip(job_status,
                          (Waiting, Running, Finished, Failed, Stopped, Queued)))


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

    def getStatus(self):
        """
        return instance of the L{JobStatus} subclasses
        """
        return JOB_STATUS_MAP[self.status](self)
