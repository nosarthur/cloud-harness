import json

from app import create_app, db
from app.models import User, Job


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
        db.session.add_all([u1, j1, j2, u2])
        db.session.commit()
        self.admin_token = u1.encode_token()
        self.token = u2.encode_token()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all(self):
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/jobs/', headers=headers):
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

    def test_get_one(self):
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/jobs/1', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            j = json.loads(res.data)
            assert j['id'] == 1
            assert j['user_id'] == 1

    def test_no_token(self):
        with self.app.test_request_context('/api/jobs/'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 400

    def test_wrong_token(self):
        headers = [('Authorization', 'Bearer ' + 'wrong token'),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/jobs/', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 400

    def test_post(self):
        headers = [('Authorization', 'Bearer ' + self.token),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/jobs/',
                                           headers=headers,
                                           data=json.dumps({'priority': 2}),
                                           method='POST'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 201
            j = json.loads(res.data)
            assert j['id'] == 3
            assert j['user_id'] == 2
            assert j['priority'] == 2

    def test_put(self):
        headers = [('Authorization', 'Bearer ' + self.token),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/jobs/1',
                                           headers=headers,
                                           data=json.dumps({'priority': 3}),
                                           method='PUT'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 204
            j = json.loads(res.data)
            assert j['id'] == 1
            assert j['priority'] == 3

    def test_delete(self):
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/jobs/1',
                                           headers=headers,
                                           method='DELETE'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 204
            j = Job.query.get(1)
            assert not j
