import pytest
import flask

from app import create_app, db
from app.models import User


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

    def test_validate_token(self):
        db.create_all()
        u = User('test', 'a@b.com', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.encode_token()
        user_id = User.decode_token(token)
        assert user_id == u.id
        assert User.validate('a@b.com', 'cat') == u
