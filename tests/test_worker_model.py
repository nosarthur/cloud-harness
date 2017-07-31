import datetime
import pytest

from app.models import Worker, Job


@pytest.mark.usefixtures('full_app')
class TestWorkerModel:
    def test_check_health(self):
        w1 = Worker.query.get(1)
        w2 = Worker.query.get(2)

        # no job_id
        assert not w2.checkHealth()

        # valid job_id
        assert w1.checkHealth()

        # expired
        w1.date_modified -= datetime.timedelta(minutes=50)
        assert not w1.checkHealth()
        j = Job.query.get(w1.job_id)
        assert j.status == 'FAILED'
