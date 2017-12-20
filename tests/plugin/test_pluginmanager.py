import os
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
