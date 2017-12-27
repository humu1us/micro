from unittest import TestCase
from micro.plugin.pluginbase import PluginBase


class TestPluginBase(TestCase):
    def test_construction(self):
        pb = PluginBase()

        with self.assertRaises(Exception) as context:
            pb.run(N="")
        self.assertEqual(type(context.exception), NotImplementedError)
