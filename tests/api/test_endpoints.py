import os
from unittest import TestCase
from micro.core.params import Params


class TestEndpoints(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.path = os.path.join(self.parent, "resources", "plugin")
        os.environ["MICRO_PLUGIN_PATH"] = self.path
        os.environ["MICRO_BROKER_URL"] = "broker_test"
        os.environ["MICRO_QUEUE_NAME"] = "queue_test"
        os.environ["MICRO_LOG_PATH"] = self.parent
        os.environ["MICRO_LOG_FROM"] = "INFO"
        Params()

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_LOG_FROM"]

    def test_plugins(self):
        from micro.api.endpoints import plugins
        self.assertEqual(plugins(),
                         {"Example Plugin": "A very simple example plugin"})

    def test_info(self):
        from micro.api.endpoints import info
        resp = "This plugin is a very simple example, " + \
               "for that reason, we don't have a long description"
        self.assertEqual(info("Example Plugin"), resp)

        self.assertIsNone(info("Non-existent plugin"))

    def test_help(self):
        from micro.api.endpoints import help
        self.assertEqual(help("Example Plugin"),
                         "Params: name type string; A name to greet")

        self.assertIsNone(help("Non-existent plugin"))

    def test_run(self):
        from micro.api.endpoints import run
        self.assertEqual(run("Example Plugin", name="World"),
                         "Hello World!!!")

        self.assertEqual(run("Non-existent plugin", name="World"),
                         "Plugin not found")
