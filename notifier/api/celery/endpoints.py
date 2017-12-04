from ...core.notifierapp import NotifierApp
from ...helper.celeryapi import celery_name
from ...helper.celeryapi import queue
from ...plugin.pluginmanager import PluginManager


app = NotifierApp.instance()
manager = PluginManager()
QUEUE = queue()


@app.task(name=celery_name("list"), queue=QUEUE)
def list():
    return manager.list()


@app.task(name=celery_name("info"), queue=QUEUE)
def info(name):
    return manager.info(name)


@app.task(name=celery_name("run"), queue=QUEUE)
def run(plugin_name, **kwargs):
    plg = manager.instance(plugin_name)
    result = plg.run(**kwargs)
    return result
