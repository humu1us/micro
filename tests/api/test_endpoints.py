import os
import json
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
        os.environ["MICRO_CELERY"] = "1"
        Params()

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_LOG_FROM"]
        del os.environ["MICRO_CELERY"]

    def test_plugins(self):
        from micro.api.endpoints import plugins
        resp = [{
            "name": "Example Plugin",
            "version": None,
            "description": "A very simple example plugin"
        }]
        self.assertEqual(plugins(), json.dumps(resp))

    def test_info(self):
        from micro.api.endpoints import info
        long_description = "This plugin is a very simple example, " + \
                           "for that reason, we don't have a long description"
        resp = {
            "name": "Example Plugin",
            "version": None,
            "url": None,
            "author": "Jhon Doe",
            "author_email": None,
            "description": "A very simple example plugin",
            "long_description": long_description
        }
        self.assertEqual(info("Example Plugin"), json.dumps(resp))

        self.assertEqual(info("Non-existent plugin"),
                         json.dumps({"error": "plugin not found"}))

    def test_help(self):
        from micro.api.endpoints import help
        resp = {
            "name": "Example Plugin",
            "version": None,
            "help": "Params: name type string; A name to greet"
        }
        self.assertEqual(help("Example Plugin"),
                         json.dumps(resp))

        self.assertEqual(help("Non-existent plugin"),
                         json.dumps({"error": "plugin not found"}))

    def test_run(self):
        from micro.api.endpoints import run
        self.assertEqual(run("Example Plugin", name="World"),
                         "Hello World!!!")

        self.assertEqual(run("Non-existent plugin", name="World"),
                         json.dumps({"error": "plugin not found"}))

        error = "run() got an unexpected keyword argument \'wrong_arg\'"
        self.assertEqual(run("Example Plugin", wrong_arg="World"),
                         json.dumps({"error": error}))
