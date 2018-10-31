import os
import shutil
from unittest import TestCase
from micro.core.params import Params
from micro.core.celeryapp import CeleryApp


class TestCeleryApp(TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.path.pardir))

        path = os.path.join(path, "resources", "test_config.json")
        os.environ["MICRO_CONFIG_FILE"] = path
        os.environ["MICRO_CELERY"] = "1"
        cls.test_folders = [
            ["MICRO_PLUGIN_PATH", "/tmp/micro_celeryapp_plugin"],
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_celeryapp_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_celeryapp_pids"]
        ]
        for f in cls.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

        Params(setall=True).set_params()

    @classmethod
    def tearDownClass(cls):
        del os.environ["MICRO_CONFIG_FILE"]
        del os.environ["MICRO_CELERY"]
        for f in cls.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

    def test_load_args(self):
        expected = ['celery',
                    '-A', 'micro.api.celery',
                    '-Q', 'queue_name',
                    '--logfile=/tmp/micro_celeryapp_logs/celery/%N.log',
                    '--pidfile=/tmp/micro_celeryapp_pids/celery/%N.pid',
                    'multi', 'start',
                    'worker1@micro',
                    'worker2@micro',
                    'worker3@micro',
                    'worker4@micro',
                    'worker5@micro',
                    'worker6@micro',
                    'worker7@micro',
                    'worker8@micro',
                    'worker9@micro',
                    'worker10@micro']

        app = CeleryApp()
        args = app._CeleryApp__load_args()
        self.assertEqual(args, expected)
