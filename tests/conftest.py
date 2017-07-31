import pytest

from app import create_app, db
from app.models import User, Job, Worker


@pytest.fixture(scope='class')
def vanilla_app(request):
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    u1 = User('u1', 'a@a.com', 'aaa')
    db.session.add(u1)
    db.session.commit()
    request.cls.u1_token = u1.encodeToken()
    request.cls.app = app
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture(scope='class')
def full_app(request):
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
    w1 = Worker('aaa', 1)
    w2 = Worker('bbb')
    db.session.add_all([u1, u2, u3, j1, j2, j3, j4, w1, w2])
    db.session.commit()
    request.cls.u1_token = u1.encodeToken()
    request.cls.u2_token = u2.encodeToken()
    request.cls.admin_token = u3.encodeToken()
    request.cls.app = app
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()
