import os
import shutil
from unittest import TestCase
from micro.core.params import Params


class TestEndpoints(TestCase):
    def setUp(self):
        self.test_folders = [
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_apirest_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_apirest_pids"]
        ]
        for f in self.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

    def tearDown(self):
        try:
            del os.environ["MICRO_PLUGIN_PATH"],
            del os.environ["_MICRO_PLUGIN_PATH"],
        except Exception:
            pass

        for f in self.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

    def test_run(self):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))
        plugins = os.path.join(parent, "resources", "plugin")
        os.environ["MICRO_PLUGIN_PATH"] = plugins
        Params(setall=True).set_params()

        from micro.plugin.pluginmanager import PluginManager
        from micro.api.endpoints import _run
        from micro.api import endpoints
        endpoints.manager = PluginManager()

        resp = _run(plugin_name="wrong plugin")
        expected = {"error": "plugin not found"}
        self.assertDictEqual(resp, expected)

        data = {"wrong_arg": "World"}
        resp = _run(plugin_name="Example Plugin", **data)
        expected = {
            "error": "run() got an unexpected keyword argument 'wrong_arg'"
        }
        self.assertDictEqual(resp, expected)

        data = {"name": "World"}
        resp = _run(plugin_name="Example Plugin", **data)
        expected = {
            "msg": "Hello World!!!"
        }
        self.assertDictEqual(resp, expected)

    def test_run_no_dict(self):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))
        plugins = os.path.join(parent, "resources", "error_plugins")
        os.environ["MICRO_PLUGIN_PATH"] = plugins
        Params(setall=True).set_params()

        from micro.plugin.pluginmanager import PluginManager
        from micro.api.endpoints import _run
        from micro.api import endpoints
        endpoints.manager = PluginManager()

        data = {"name": "World"}
        resp = _run(plugin_name="Example Plugin No Dict", **data)
        error_msg = "Micro plugins must return a Python dictionary"
        msg = "Hello World!!!"
        expected = {
            "error": "%s, type: %s, value: %s" % (error_msg, type(msg), msg)
        }
        self.assertDictEqual(resp, expected)
