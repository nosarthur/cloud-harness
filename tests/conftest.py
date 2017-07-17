import pytest

from app import create_app, db


@pytest.fixture(scope='module')
def myapp():
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    u1 = User('u1', 'a@a.com', 'aaa', True)  # admin
    u2 = User('u2', 'b@a.com', 'aaa')
    j1 = Job(1)
    j2 = Job(2, 3)
    db.session.add_all([u1, j1, j2, u2])
    db.session.commit()
    yield app
    db.session.remove()
    db.drop_all()
    app_context.pop()
