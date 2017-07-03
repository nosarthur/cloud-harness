import json

from app import create_app, db
from app.models import User, Job


class TestAPI:
    def setup(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        u1 = User('u1', 'a@a.com', 'aaa')
        u2 = User('u2', 'b@a.com', 'aaa')
        j1 = Job(1)
        j2 = Job(2, 3)
        db.session.add_all([u1, j1, j2, u2])
        db.session.commit()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get(self):
        with self.app.test_request_context('/jobs/', method='GET'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            jobs = json.loads(res.data)
            assert len(jobs) == 2
            j1, j2 = jobs
            assert j1['priority'] == 0
            assert j2['priority'] == 3
            assert j1['status'] == 'WAITING'
            assert j2['status'] == 'WAITING'
            assert j1['id'] == 1
            assert j2['id'] == 2
            assert j1['user_id'] == 1
            assert j2['user_id'] == 2

    def test_token_error(self):
        with self.app.test_request_context('/jobs/'):
            pass

    def test_token_approve(self):
        pass
