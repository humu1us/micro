from celery.utils.log import get_task_logger
from ..core.celery import NotifierApp

app = NotifierApp.instance()
log = get_task_logger(__name__)


@app.task(queue="notifier_queue")
def add(x, y):
    log.info("Starting task with: %s" % locals())
    return x + y
