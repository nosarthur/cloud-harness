import pytest

from driver.driver import JobControl
from app.models import Job


'''
@pytest.mark.usefixtures('vanilla_app')
class TestDriver:
    def testLogin(self):
        jc = JobControl()
        # wrong credential
        assert jc.login('a@a.com', 'aaaa')
        # correct credential
        assert jc.login('a@a.com', 'aaa')

    def testSubmit(self):
        jc = JobControl()
        # not logged in
        assert jc.submit() == 1

        jc.login('a@a.com', 'aaa')
        assert not jc.submit()
        j = Job.query.get(1)
        assert j.id == 1
'''
