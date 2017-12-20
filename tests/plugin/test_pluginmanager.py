import os
import io
import sys
from unittest import TestCase
from micro.plugin.pluginmanager import PluginManager


class TestPluginManager(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_contructor(self):
        try:
            del os.environ["MICRO_PLUGIN_PATH"]
        except:
            pass

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

    def test_mamasan(self):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))
        path = os.path.join(parent, "resources", "error_plugins")
        os.environ["MICRO_PLUGIN_PATH"] = path
        stdout = sys.stdout
        sys.stdout = io.StringIO()

        PluginManager()

        output = sys.stdout.getvalue()
        sys.stdout = stdout
        self.assertEqual(output.strip(),
                         "Error, no name set, cannot be loaded")
