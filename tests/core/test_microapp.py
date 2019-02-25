import os
import shutil
from unittest import TestCase
from testfixtures import LogCapture
from micro.core import microapp
from micro.core.microapp import MicroApp
from micro.core.params import Params
from tests.utils.fakestdout import StdoutLock


def fake_start_celery():
    print(os.getpid())


def fake_start_gunicorn():
    print(os.getpid())


class TestMicroApp(TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.path.pardir))

        path = os.path.join(path, "resources", "test_config.json")
        os.environ["MICRO_CONFIG_FILE"] = path
        os.environ["MICRO_CELERY"] = "1"
        os.environ["MICRO_GUNICORN"] = "1"
        cls.test_folders = [
            ["MICRO_PLUGIN_PATH", "/tmp/micro_microapp_plugin"],
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_microapp_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_microapp_pids"]
        ]
        for f in cls.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

        Params(setall=True).set_params()

    @classmethod
    def tearDownClass(cls):
        del os.environ["MICRO_CONFIG_FILE"]
        del os.environ["MICRO_CELERY"]
        del os.environ["MICRO_GUNICORN"]
        for f in cls.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

    def test_nothing(self):
        del os.environ["_MICRO_CELERY"]
        del os.environ["_MICRO_GUNICORN"]
        app = MicroApp()
        with StdoutLock() as lock:
            with LogCapture("Micro") as logs:
                app.start()
        no_celery = ("Micro", "WARNING", "CeleryApp not started")
        no_gunicorn = ("Micro", "WARNING", "GunicornApp not started")
        logs.check(no_celery, no_gunicorn)

        celery_msg = "CeleryApp not started"
        gunicorn_msg = "GunicornApp not started"
        lock_msgs = lock.stdout.strip().split("\n")
        self.assertEqual(lock_msgs[0], celery_msg)
        self.assertEqual(lock_msgs[1], gunicorn_msg)

    def test_start_celery(self):
        app = MicroApp()
        start_celery_aux = microapp.start_celery
        microapp.start_celery = fake_start_celery

        app._MicroApp__celery = True
        with StdoutLock() as lock:
            app.start()
        celery_msg = "Starting CeleryApp"
        gunicorn_msg = "GunicornApp not started"
        lock_msgs = lock.stdout.strip().split("\n")
        self.assertEqual(lock_msgs[0], celery_msg)
        self.assertEqual(lock_msgs[1], gunicorn_msg)

        microapp.start_celery = start_celery_aux

    def test_start_gunicorn(self):
        app = MicroApp()
        start_gunicorn_aux = microapp.start_gunicorn
        microapp.start_gunicorn = fake_start_gunicorn

        app._MicroApp__gunicorn = True
        with StdoutLock() as lock:
            app.start()
        celery_msg = "CeleryApp not started"
        gunicorn_msg = "Starting GunicornApp"
        lock_msgs = lock.stdout.strip().split("\n")
        self.assertEqual(lock_msgs[0], celery_msg)
        self.assertEqual(lock_msgs[1], gunicorn_msg)

        microapp.start_gunicorn = start_gunicorn_aux
