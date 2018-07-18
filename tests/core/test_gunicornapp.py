import os
from unittest import TestCase
from flask import Flask
from micro.core.params import Params


class TestConfig(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.file = os.path.join(self.parent, "resources", "test_config.json")
        self.bind = "localhost:3050"
        self.num_workers = 5
        os.environ["MICRO_PLUGIN_PATH"] = self.parent
        os.environ["MICRO_BROKER_URL"] = "broker_test"
        os.environ["MICRO_QUEUE_NAME"] = "queue_test"
        os.environ["MICRO_NUM_WORKERS"] = str(self.num_workers)
        os.environ["MICRO_GUNICORN_BIND"] = self.bind
        os.environ["MICRO_LOG_PATH"] = self.parent
        os.environ["MICRO_GUNICORN"] = "1"
        Params()

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_NUM_WORKERS"]
        del os.environ["MICRO_GUNICORN_BIND"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_GUNICORN"]

    def test_load_config(self):
        from micro.core.gunicornapp import GunicornApp
        app = GunicornApp()
        app.load_config()
        self.assertEqual(app.cfg.bind[0], self.bind)
        self.assertEqual(app.cfg.workers, self.num_workers)
        self.assertTrue(app.cfg.daemon)

    def test_load(self):
        from micro.core.gunicornapp import GunicornApp
        app = GunicornApp()
        flask_app = app.load()
        self.assertTrue(isinstance(flask_app, Flask))
