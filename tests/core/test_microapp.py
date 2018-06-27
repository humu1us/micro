import os
from unittest import TestCase
from micro.core import microapp
from micro.core.microapp import MicroApp


def fake_start_celery():
    print(os.getpid())


class TestMicroApp(TestCase):
    def test_run_celery(self):
        app = MicroApp()
        start_celery_aux = microapp.start_celery
        microapp.start_celery = fake_start_celery

        app.start()

        microapp.start_celery = start_celery_aux
