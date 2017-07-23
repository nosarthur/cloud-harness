import pytest

from app.models import User


class TestUserModel:
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


@pytest.mark.usefixtures('vanilla_app')
class TestUserDB:
    def test_validate_token(self):
        u = User.query.get(1)
        token = u.encode_token()
        user_id = User.decode_token(token)
        assert user_id == u.id
        assert User.validate('a@a.com', 'aaa') == u
