from datetime import timedelta

import celery
from main.celery import app
import logging

from social.models import Crown
from main.utils import MINUTES

logger = logging.getLogger(__name__)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

# @celery.task(default_retry_delay=10 * MINUTES, max_retries=10)
@app.task
def create_result_last_week():
    # try:
    print('i am task wtf')
    #     Crown.create_result_last_week()
    # except Exception as e:
    #     logger.error(str(e))
    #     raise create_result_last_week.retry(e)
