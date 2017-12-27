import os
from unittest import TestCase
from testfixtures import LogCapture


class TestPluginManager(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        os.environ["MICRO_LOG_PATH"] = self.parent
        os.environ["MICRO_LOG_FROM"] = "INFO"

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_LOG_FROM"]

    def test_contructor(self):
        from micro.plugin.pluginmanager import PluginManager

        with self.assertRaises(Exception) as context:
            PluginManager()
        self.assertEqual(type(context.exception), RuntimeError)

        os.environ["MICRO_PLUGIN_PATH"] = "this_is_not_a_path"

        with self.assertRaises(Exception) as context:
            PluginManager()
        self.assertEqual(type(context.exception), RuntimeError)

        os.environ["MICRO_PLUGIN_PATH"] = "/"
        pm = PluginManager()
        self.assertEqual(type(pm), PluginManager)

    def test_error_plugins(self):
        path = os.path.join(self.parent, "resources", "error_plugins")
        os.environ["MICRO_PLUGIN_PATH"] = path
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
