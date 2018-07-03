import os
from unittest import TestCase
from testfixtures import LogCapture
from micro.core import microapp
from micro.core.microapp import MicroApp
from micro.core.params import Params


def fake_start_celery():
    print(os.getpid())


class TestMicroApp(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.path = os.path.join(self.parent, "resources", "plugin")
        os.environ["MICRO_PLUGIN_PATH"] = self.path
        os.environ["MICRO_BROKER_URL"] = "broker_test"
        os.environ["MICRO_QUEUE_NAME"] = "queue_test"
        os.environ["MICRO_LOG_PATH"] = self.parent
        os.environ["MICRO_CELERY"] = "1"
        os.environ["MICRO_GUNICORN"] = "1"
        Params()

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_CELERY"]
        del os.environ["MICRO_GUNICORN"]

    def test_nothing(self):
        del os.environ["_MICRO_CELERY"]
        del os.environ["_MICRO_GUNICORN"]
        app = MicroApp()
        with LogCapture("Micro") as logs:
            app.start()
        no_celery = ("Micro", "WARNING", "CeleryApp not started")
        no_gunicorn = ("Micro", "WARNING", "GunicornApp not started")
        logs.check(no_celery, no_gunicorn)

    def test_start_celery(self):
        app = MicroApp()
        start_celery_aux = microapp.start_celery
        microapp.start_celery = fake_start_celery

        app._MicroApp__start_celery()

        microapp.start_celery = start_celery_aux
