from datetime import timedelta, date, datetime

import celery
import logging

from celery.schedules import crontab

from social.models import Crown, RequestDonations

logger = logging.getLogger(__name__)


@celery.task.periodic_task(run_every=crontab(hour=00, minute=1, day_of_week=1))
def create_result_last_week():
    try:
        Crown.create_result_last_week()
    except Exception as e:
        logger.error(str(e))
        raise create_result_last_week.retry(e)


@celery.task.periodic_task(run_every=timedelta(hours=1))
def check_expired_request_donate():
    try:
        RequestDonations.objects.filter(expired_at__lte=datetime.now()).update(is_active=False)
    except Exception as e:
        raise logger.error(str(e))
