import pytest

from app import create_app, db


class TestAPI:
    def setup(self):
        self.app = create_app('testing')
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test(self):
        pass
