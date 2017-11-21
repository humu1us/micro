from celery import Celery
from ..conf import config

app = Celery(config.app_name)

app.conf.update(broker_url=config.broker_url,
                result_backend="rpc://")
