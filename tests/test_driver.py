import pytest

from driver.driver import JobControl


@pytest.mark.usefixtures('vanilla_app')
class TestDriver:
    def testLogin(self):
        jc = JobControl()
        assert jc
