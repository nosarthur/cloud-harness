import pytest
import json

# from app.models import Worker


@pytest.mark.usefixtures('full_app')
class TestAPI1:
    """
    Functions in this class do not change the database.
    """
    def test_get_all(self):
        # as administrator
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/workers/', headers=headers):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            workers = json.loads(res.data)
            assert len(workers) == 2
            w1, w2 = workers
            assert w1['id'] == 1
            assert w2['id'] == 2
            assert w1['job_id'] == 1
            assert not w2['job_id']

# FIXME: for now all users can see all workers

# The following classes contain functions that change the database


@pytest.mark.usefixtures('full_app')
class TestAPI2:
    def test_delete(self):
        # FIXME: AWS access should be mocked
        return
        # u2 cannot delete w1
        headers = [('Authorization', 'Bearer ' + self.u2_token),
                   ('Content-Type', 'application/json')]
        with self.app.test_request_context('/api/workers/1',
                                           headers=headers,
                                           method='DELETE'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 400

        # u1 can delete w1
        headers = [('Authorization', 'Bearer ' + self.u1_token)]
        with self.app.test_request_context('/api/workers/',
                                           headers=headers,
                                           method='DELETE'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200

        # admin can delete anything
        headers = [('Authorization', 'Bearer ' + self.admin_token)]
        with self.app.test_request_context('/api/jobs/2',
                                           headers=headers,
                                           method='DELETE'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 204
