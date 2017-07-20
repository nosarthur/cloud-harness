import pytest
import json

from app.models import Job


@pytest.mark.usefixtures('myapp')
class TestAPI1:
    """
    Functions in this class do not change the database.
    """
    def test_get_all(self):
        # as administrator
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/jobs/', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            jobs = json.loads(res.data)
            assert len(jobs) == 4
            j1, j2, j3, j4 = jobs
            assert j1['priority'] == 0
            assert j2['priority'] == 3
            assert j3['priority'] == 0
            assert j4['priority'] == 0
            assert j1['status'] == 'WAITING'
            assert j2['status'] == 'WAITING'
            assert j3['status'] == 'RUNNING'
            assert j4['status'] == 'WAITING'
            assert j1['id'] == 1
            assert j2['id'] == 2
            assert j3['id'] == 3
            assert j4['id'] == 4
            assert j1['user_id'] == 1
            assert j2['user_id'] == 2
            assert j3['user_id'] == 2
            assert j4['user_id'] == 3

        # as user 1
        headers = [('Authorization', 'Bearer ' + self.u1_token)]
        with self.app.test_request_context('/api/jobs/', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            jobs = json.loads(res.data)
            assert len(jobs) == 1
            j1 = jobs[0]
            assert j1['id'] == 1

        # as user 2
        headers = [('Authorization', 'Bearer ' + self.u2_token)]
        with self.app.test_request_context('/api/jobs/', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            jobs = json.loads(res.data)
            assert len(jobs) == 2
            j2, j3 = jobs
            assert j2['id'] == 2
            assert j3['id'] == 3

    def test_get_one(self):
        # admin gets everything
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/jobs/1', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            j = json.loads(res.data)
            assert j['id'] == 1
            assert j['user_id'] == 1

        # user1 gets job1
        headers = [('Authorization', 'Bearer ' + self.u1_token)]
        with self.app.test_request_context('/api/jobs/1', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            j = json.loads(res.data)
            assert j['id'] == 1
            assert j['user_id'] == 1

        # user1 cannot get job2
        headers = [('Authorization', 'Bearer ' + self.u1_token)]
        with self.app.test_request_context('/api/jobs/2', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 400

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

# The following classes contain functions that change the database


@pytest.mark.usefixtures('myapp')
class TestAPI2:
    def test_delete(self):
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/jobs/1',
                                           headers=headers,
                                           method='DELETE'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 204
            j = Job.query.get(1)
            assert not j

        # u2 cannot change job 1
        headers = [('Authorization', 'Bearer ' + self.u2_token),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/jobs/1',
                                           headers=headers,
                                           method='DELETE'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 400


@pytest.mark.usefixtures('myapp')
class TestAPI3:
    def test_put(self):
        # u2 can change job 2
        headers = [('Authorization', 'Bearer ' + self.u2_token),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/jobs/2',
                                           headers=headers,
                                           data=json.dumps({'priority': 5}),
                                           method='PUT'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 204
            j = json.loads(res.data)
            assert j['id'] == 2
            assert j['priority'] == 5

        # u2 cannot change job 1
        headers = [('Authorization', 'Bearer ' + self.u2_token),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/jobs/1',
                                           headers=headers,
                                           data=json.dumps({'priority': 3}),
                                           method='PUT'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 400


@pytest.mark.usefixtures('myapp')
class TestAPI4:
    def test_post(self):
        headers = [('Authorization', 'Bearer ' + self.u2_token),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/jobs/',
                                           headers=headers,
                                           data=json.dumps({'priority': 2}),
                                           method='POST'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 201
            j = json.loads(res.data)
            assert j['id'] == 5
            assert j['user_id'] == 2
            assert j['priority'] == 2
