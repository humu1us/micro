import os
from unittest import TestCase
from testfixtures import LogCapture
from micro.core.params import Params
from micro.plugin.pluginmanager import PluginManager


class TestPluginManager(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.path = os.path.join(self.parent, "resources", "plugin")
        os.environ["MICRO_BROKER_URL"] = "broker_test"
        os.environ["MICRO_QUEUE_NAME"] = "queue_test"
        os.environ["MICRO_LOG_PATH"] = self.parent
        os.environ["MICRO_CELERY"] = "1"

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_CELERY"]

    def test_contructor(self):
        os.environ["MICRO_PLUGIN_PATH"] = "this_is_not_a_path"
        Params()

        with self.assertRaises(SystemExit) as se:
            PluginManager()

        err = "ERROR: plugins path no name a folder: "
        err += "this_is_not_a_path"
        self.assertEqual(se.exception.args[0], err)

        os.environ["MICRO_PLUGIN_PATH"] = "/"
        Params()
        pm = PluginManager()
        self.assertEqual(type(pm), PluginManager)

    def test_error_plugins(self):
        path = os.path.join(self.parent, "resources", "error_plugins")
        os.environ["MICRO_PLUGIN_PATH"] = path
        Params()

        with LogCapture("Micro") as logs:
            PluginManager()
        logs.check(
            ("Micro",
             "INFO",
             "Load plugins from: " + path),
            ("Micro",
             "INFO",
             "Load plugins, checking: " + path + "/example_noname"),
            ("Micro",
             "WARNING",
             "Plugin " + path + "/example_noname " +
             "does not has name. Omitted"),
            ("Micro",
             "INFO",
             "Load plugins, checking: " + path + "/example_notype"),
            ("Micro",
             "WARNING",
             "Plugin " + path + "/example_notype " + "is not valid. Omitted")
        )
