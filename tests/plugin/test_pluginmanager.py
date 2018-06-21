import os
from unittest import TestCase
from testfixtures import LogCapture
from micro.core.params import Params
from tests.utils.fakestdout import StdoutLock


class TestPluginManager(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        config = os.path.join(self.parent, "resources", "test_config.json")
        os.environ["MICRO_BROKER_URL"] = "test"
        os.environ["MICRO_QUEUE_NAME"] = "test"
        os.environ["MICRO_CONFIG"] = config

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_CONFIG"]

    def test_contructor(self):
        os.environ["MICRO_PLUGIN_PATH"] = "this_is_not_a_path"
        Params()

        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                from micro.plugin.pluginmanager import PluginManager
                PluginManager()

        err = "ERROR: plugins path no name a folder: "
        err += "this_is_not_a_path"
        self.assertEqual(lock.stderr, err)

        os.environ["MICRO_PLUGIN_PATH"] = "/"
        Params()
        pm = PluginManager()
        self.assertEqual(type(pm), PluginManager)

    def test_error_plugins(self):
        path = os.path.join(self.parent, "resources", "error_plugins")
        os.environ["MICRO_PLUGIN_PATH"] = path
        Params()
        from micro.plugin.pluginmanager import PluginManager

        with LogCapture() as logs:
            PluginManager()
        logs.check(
            ("root",
             "INFO",
             "Load plugins from: " + path),
            ("root",
             "INFO",
             "Load plugins, checking: " + path + "/example_noname"),
            ("root",
             "WARNING",
             "Plugin " + path + "/example_noname " +
             "does not has name. Omitted"),
            ("root",
             "INFO",
             "Load plugins, checking: " + path + "/example_notype"),
            ("root",
             "WARNING",
             "Plugin " + path + "/example_notype " + "is not valid. Omitted")
        )
