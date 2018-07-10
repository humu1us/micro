from .endpoints import _help
from .endpoints import _info
from .endpoints import _plugins
from .endpoints import _run
from ..core.celeryapp import CeleryApp

app = CeleryApp()


@app.task(name=app.function_name("plugins"), queue=app.queue())
def plugins():
    return _plugins()


@app.task(name=app.function_name("info"), queue=app.queue())
def info(name):
    return _info(name)


@app.task(name=app.function_name("help"), queue=app.queue())
def help(name):
    return _help(name)


@app.task(name=app.function_name("run"), queue=app.queue())
def run(plugin_name, **kwargs):
    return _run(plugin_name, **kwargs)
