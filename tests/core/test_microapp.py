import os
from unittest import TestCase
from micro.core import microapp
from micro.core.microapp import MicroApp
from tests.utils.fakestdout import StdoutLock


def fake_start_celery():
    print(os.getpid())


class TestMicroApp(TestCase):
    def test_nothing(self):
        no_celery = "CeleryApp not started"
        no_flask = "FlaskApp not started"
        msg = no_celery + "\n" + no_flask

        app = MicroApp()
        with StdoutLock() as lock:
            app.start()
        self.assertEqual(lock.stdout.rstrip(), msg)

    def test_start_celery(self):
        app = MicroApp()
        app._MicroApp__celery = True
        start_celery_aux = microapp.start_celery
        microapp.start_celery = fake_start_celery

        app._MicroApp__start_celery()

        microapp.start_celery = start_celery_aux
