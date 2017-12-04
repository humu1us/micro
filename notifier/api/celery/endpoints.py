from ...core.notifierapp import NotifierApp
from ...helper.celeryapi import celery_name
from ...helper.celeryapi import queue
from ...plugin.pluginloader import PluginLoader


app = NotifierApp.instance()
plugin_loader = PluginLoader()
QUEUE = queue()


@app.task(name=celery_name("list"), queue=QUEUE)
def list():
    return plugin_loader.list()


@app.task(name=celery_name("info"), queue=QUEUE)
def info(name):
    return plugin_loader.info(name)


@app.task(name=celery_name("run"), queue=QUEUE)
def run(plugin_name, **kwargs):
    plg = plugin_loader.instance(plugin_name)
    result = plg.run(**kwargs)
    return result
