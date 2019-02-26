from ..core.logger import Logger
from ..plugin.pluginmanager import PluginManager

log = Logger()
manager = PluginManager()


def _plugins():
    log.info("Endpoint call: Micro.plugins()")
    return manager.plugins()


def _info(name):
    log.info("Endpoint call: Micro.info(%s)" % name)
    return manager.info(name)


def _help(name):
    log.info("Endpoint call: Micro.help(%s)" % name)
    return manager.help(name)


def _run(plugin_name, **kwargs):
    log.info("Endpoint call: Micro.run(%s, %s)" % (plugin_name, kwargs))
    plg = manager.instance(plugin_name)
    if not plg:
        msg = "plugin not found"
        log.error(msg)
        return {"error": msg}

    try:
        result = plg.run(**kwargs)
    except TypeError as e:
        log.error(str(e))
        return {"error": str(e)}

    if not isinstance(result, dict):
        msg = "Micro plugins must return a Python dictionary"
        response = "%s, type: %s, value: %s" % (msg, type(result), str(result))
        log.error(response)
        return {"error": response}

    return result
