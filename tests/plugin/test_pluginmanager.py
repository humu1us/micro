import os
import shutil
from unittest import TestCase
from testfixtures import LogCapture
from micro.core.params import Params
from micro.plugin.pluginmanager import PluginManager


class TestPluginManager(TestCase):
    @classmethod
    def setUpClass(cls):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))

        path = os.path.join(parent, "resources", "test_config.json")
        cls.plugins = os.path.join(parent, "resources", "error_plugins")
        os.environ["MICRO_CONFIG_FILE"] = path
        cls.test_folders = [
            ["MICRO_PLUGIN_PATH", cls.plugins],
            ["MICRO_LOG_LEVEL", "INFO"],
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_plgmng_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_plgmng_pids"]
        ]
        for f in cls.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

        Params(setall=True).set_params()

    @classmethod
    def tearDownClass(cls):
        del os.environ["MICRO_CONFIG_FILE"]
        for f in cls.test_folders:
            del os.environ[f[0]]
            if f[1] == cls.plugins:
                continue
            shutil.rmtree(f[1])

    def test_contructor(self):
        pm = PluginManager()
        self.assertEqual(type(pm), PluginManager)

    def test_error_plugins(self):
        path = self.plugins
        with LogCapture("Micro") as logs:
            PluginManager()
        logs.check_present(
            ("Micro",
             "INFO",
             "Load plugins from: "
             + path + ""),
            ("Micro",
             "INFO",
             "Load plugins, checking: "
             + path + "/example_nointerface"),
            ("Micro",
             "WARNING",
             "Plugin "
             + path + "/example_nointerface "
             "is not valid. Omitted"),
            ("Micro",
             "INFO",
             "Load plugins, checking: "
             + path + "/example_noname"),
            ("Micro",
             "WARNING",
             "Plugin "
             + path + "/example_noname "
             "does not has name. Omitted"),
            ("Micro",
             "INFO",
             "Load plugins, checking: "
             + path + "/example_notype"),
            ("Micro",
             "WARNING",
             "Plugin "
             + path + "/example_notype "
             "is not valid. Omitted"),
            ("Micro",
             "INFO",
             "Load plugins, checking: "
             + path + "/file_to_ommit"),
            ("Micro",
             "WARNING",
             "File found in the plugins folder: "
             + path + "/file_to_ommit. "
             "Omitted"),
            order_matters=False
        )
