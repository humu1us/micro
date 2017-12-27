from ..core.microapp import MicroApp
from ..plugin.pluginmanager import PluginManager
from ..core.logger import log


app = MicroApp()
manager = PluginManager()


@app.task(name=app.function_name("plugins"), queue=app.queue())
def plugins():
    log.info("Endpoint call: Micro.plugins()")
    return manager.plugins()


@app.task(name=app.function_name("info"), queue=app.queue())
def info(name):
    log.info("Endpoint call: Micro.info(%s)" % name)
    return manager.info(name)


@app.task(name=app.function_name("help"), queue=app.queue())
def help(name):
    log.info("Endpoint call: Micro.help(%s)" % name)
    return manager.help(name)


@app.task(name=app.function_name("run"), queue=app.queue())
def run(plugin_name, **kwargs):
    log.info("Endpoint call: Micro.run(%s, %s)" % (plugin_name, kwargs))
    plg = manager.instance(plugin_name)
    if not plg:
        return "Plugin not found"
    result = plg.run(**kwargs)
    return result
