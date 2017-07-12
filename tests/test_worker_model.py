import datetime
from app import create_app, db
from app.models import Worker, Job, User


class TestWorkerModel:
    def setup(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_check_health(self):
        db.create_all()
        w = Worker('1.1.1.1', 0.2)
        j = Job(1)
        u = User('u1', 'a@a.com', 'aaa', True)  # admin
        db.session.add_all([w, j, u])
        db.session.commit()

        # no job_id
        assert not w.check_health()
        assert j.status == 'WAITING'

        # valid job_id
        w.job_id = 1
        db.session.commit()
        assert w.check_health()

        # expired
        w.date_modified -= datetime.timedelta(minutes=50)
        assert not w.check_health()
        assert j.status == 'FAILED'
