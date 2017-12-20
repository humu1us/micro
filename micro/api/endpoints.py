from ..core.microapp import MicroApp
from ..plugin.pluginmanager import PluginManager


app = MicroApp()
manager = PluginManager()


@app.task(name=app.function_name("plugins"), queue=app.queue())
def plugins():
    return manager.plugins()


@app.task(name=app.function_name("info"), queue=app.queue())
def info(name):
    return manager.info(name)


@app.task(name=app.function_name("help"), queue=app.queue())
def help(name):
    return manager.help(name)


@app.task(name=app.function_name("run"), queue=app.queue())
def run(plugin_name, **kwargs):
    plg = manager.instance(plugin_name)
    result = plg.run(**kwargs)
    return result
