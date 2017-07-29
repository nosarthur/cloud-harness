from flask_restful import Resource

from ..models import Job, Worker


class SummaryAPI(Resource):
    """
    Summaries without authentication.
    """
    def get(self):
        waiting = Job.query.filter_by(status='WAITING').count()
        running = Job.query.filter_by(status='RUNNING').count()
        finished = Job.query.filter_by(status='FINISHED').count()
        failed = Job.query.filter_by(status='FAILED').count()

        working = Worker.query.filter_by(date_finished=None).count()
        completed = Worker.query.filter(
                                    Worker.date_finished.isnot(None)).count()

        return {'jobs': {'waiting': waiting,
                         'running': running,
                         'finished': finished,
                         'failed': failed, },
                'workers': {'active': working,
                            'inactive': completed, }
                }
