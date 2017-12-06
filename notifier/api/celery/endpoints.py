from ...core.notifierapp import NotifierApp
from ...helper.celeryapi import celery_name
from ...plugin.pluginmanager import PluginManager


app = NotifierApp()
manager = PluginManager(app.plugin_path())


@app.task(name=celery_name("list"), queue=app.queue())
def list():
    return manager.list()


@app.task(name=celery_name("info"), queue=app.queue())
def info(name):
    return manager.info(name)


@app.task(name=celery_name("run"), queue=app.queue())
def run(plugin_name, **kwargs):
    plg = manager.instance(plugin_name)
    result = plg.run(**kwargs)
    return result
