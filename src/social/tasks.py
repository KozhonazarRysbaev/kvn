from datetime import timedelta

import celery
import logging

from celery.schedules import crontab

from social.models import Crown

logger = logging.getLogger(__name__)


@celery.task.periodic_task(run_every=crontab(hour=00, minute=1, day_of_week=1))
def create_result_last_week():
    try:
        Crown.create_result_last_week()
    except Exception as e:
        logger.error(str(e))
        raise create_result_last_week.retry(e)
