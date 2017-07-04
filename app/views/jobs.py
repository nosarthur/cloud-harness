from flask import Blueprint
from flask_login import login_required, current_user

from ..models import Job

jobs = Blueprint('jobs', __name__)


@jobs.route('/')
@login_required
def index():
    """
    Return jobs owned by the current user
    """
    if current_user.is_authenticated():
        if current_user.is_admin:
            res = Job.query.all()
        else:
            res = Job.query.filter_by(user_id=current_user.id)
# FIXME: maybe jsonify?
    return res


