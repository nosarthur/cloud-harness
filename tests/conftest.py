import pytest

from app import create_app, db
from app.models import User, Job, Worker


@pytest.fixture(scope='class')
def myapp(request):
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    u1 = User('u1', 'a@a.com', 'aaa')
    u2 = User('u2', 'b@a.com', 'aaa')
    u3 = User('u3', 'c@a.com', 'aaa', True)  # admin
    j1 = Job(1)
    j2 = Job(2, 3)
    j3 = Job(2)
    j3.status = 'RUNNING'
    j4 = Job(3)
    w1 = Worker('aaa', 0.3)
    w1.job_id = 1
    w2 = Worker('bbb', 0.3)
    w2.job_id = 2
    db.session.add_all([u1, u2, u3, j1, j2, j3, j4, w1, w2])
    db.session.commit()
    request.cls.u1_token = u1.encode_token()
    request.cls.u2_token = u2.encode_token()
    request.cls.admin_token = u3.encode_token()
    request.cls.app = app
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()
