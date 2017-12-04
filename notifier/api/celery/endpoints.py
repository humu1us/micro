from ...core.notifierapp import NotifierApp
from ...helper.celeryapi import celery_name
from ...helper.celeryapi import queue
from ...plugin.pluginloader import PluginLoader


app = NotifierApp.instance()
plugin_loader = PluginLoader()
QUEUE = queue()


@app.task(name=celery_name("plugin_list"), queue=QUEUE)
def plugin_list():
    return plugin_loader.list_all()


@app.task(name=celery_name("plugin_info"), queue=QUEUE)
def plugin_info(name):
    return plugin_loader.long_description(name)


@app.task(name=celery_name("notify"), queue=QUEUE)
def notify(plugin_name, **kwargs):
    plg = plugin_loader.instance(plugin_name)
    result = plg.run(**kwargs)
    return result
