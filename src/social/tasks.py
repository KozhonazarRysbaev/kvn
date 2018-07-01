from datetime import timedelta

import celery
import logging

from main.utils import MINUTES

logger = logging.getLogger(__name__)


@celery.task(default_retry_delay=10 * MINUTES, max_retries=10)
@celery.task.periodic_task(run_every=timedelta(days=7))
def user_king():
    print("king")
