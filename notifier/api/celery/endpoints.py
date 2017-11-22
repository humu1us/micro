from ...core.notifierapp import NotifierApp
from ...helper.celeryapi import celery_name
from ...helper.celeryapi import queue
from ...core.apiimpl import ApiImpl


app = NotifierApp.instance()
api = ApiImpl()
QUEUE = queue()


@app.task(name=celery_name("plugin_list"), queue=QUEUE)
def plugin_list():
    return api.plugin_list()


@app.task(name=celery_name("plugin_info"), queue=QUEUE)
def plugin_info(name):
    return api.plugin_info(name)


@app.task(name=celery_name("notify"), queue=QUEUE)
def notify():
    return api.notify()
