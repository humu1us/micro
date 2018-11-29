import json
from .endpoints import _help
from .endpoints import _info
from .endpoints import _plugins
from .endpoints import _run
from ..core.celeryapp import CeleryApp

app = CeleryApp()


@app.task(name=app.function_name("plugins"), queue=app.queue())
def plugins():
    return json.dumps(_plugins())


@app.task(name=app.function_name("info"), queue=app.queue())
def info(name):
    return json.dumps(_info(name))


@app.task(name=app.function_name("help"), queue=app.queue())
def help(name):
    return json.dumps(_help(name))


@app.task(name=app.function_name("run"), queue=app.queue())
def run(plugin_name, **kwargs):
    resp = _run(plugin_name, **kwargs)
    try:
        resp = json.loads(resp)
    except ValueError:
        pass

    return json.dumps(resp)
