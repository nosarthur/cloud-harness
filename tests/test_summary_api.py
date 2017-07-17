import json

from app import create_app, db
from app.models import User, Job, Worker


class TestAPI:
    def setup(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        u1 = User('u1', 'a@a.com', 'aaa', True)  # admin
        u2 = User('u2', 'b@a.com', 'aaa')
        j1 = Job(1)
        j2 = Job(2, 3)
        w1 = Worker('0.0.0.0', 0.3)
        db.session.add_all([u1, j1, j2, u2, w1])
        db.session.commit()
        self.admin_token = u1.encode_token()
        self.token = u2.encode_token()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_summary(self):
        with self.app.test_request_context('/api/summary'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            summary = json.loads(res.data)
            assert summary == {u'workers': {u'working': 1, u'finished': 0},
                               u'jobs': {u'running': 0, u'failed': 0,
                                         u'waiting': 2, u'finished': 0}}

 
