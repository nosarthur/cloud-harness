import pytest
import flask

from app import create_app, db
from app.models import User, load_user, load_user_from_request


class TestUserModel:
    def setup(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User('test', 'a@b.com', password='cat')
        assert u.password_hash

    def test_no_password_getter(self):
        u = User('test', 'a@b.com', password='cat')
        with pytest.raises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User('test', 'a@b.com', password='cat')
        assert u.verify_password('cat')
        assert not u.verify_password('dog')

    def test_user_loader(self):
        db.create_all()
        u = User('test', 'a@b.com', password='cat')
        db.session.add(u)
        db.session.commit()
        assert load_user(u.id) == u
        assert not load_user(100)

    def test_request_loader(self):
        db.create_all()
        u = User('test', 'a@b.com', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.encode_token()
        headers = [('Authorization', 'Bearer ' + token)]
        with self.app.test_request_context('/', headers=headers):
            assert load_user_from_request(flask.request) == u

    def test_validate_token(self):
        db.create_all()
        u = User('test', 'a@b.com', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.encode_token()
        user_id = User.decode_token(token)
        assert user_id == u.id
        assert User.validate('a@b.com', 'cat') == u
