import json
import pytest


@pytest.mark.usefixtures('full_app')
class TestAPI:
    def test_get_summary(self):
        with self.app.test_request_context('/api/summary'):
            res = self.app.full_dispatch_request()
            assert res.status_code == 200
            summary = json.loads(res.data)
            assert summary == {u'workers': {
                                    u'inactive': 0, u'active': 2},
                               u'jobs': {
                                    u'running': 1, u'failed': 0,
                                    u'waiting': 3, u'finished': 0}}
