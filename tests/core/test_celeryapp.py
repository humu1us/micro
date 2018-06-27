import os
from unittest import TestCase
from micro.core.params import Params
from micro.core.celeryapp import CeleryApp


class TestCeleryApp(TestCase):
    def setUp(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.path.pardir))

        path = os.path.join(path, "resources", "test_config.json")
        os.environ["MICRO_CONFIG"] = path
        Params()

    def tearDown(self):
        del os.environ["MICRO_CONFIG"]

    def test_load_args(self):
        expected = ['celery',
                    '-A', 'micro.api.endpoints',
                    '-Q', 'queue_name',
                    '-b', 'test://user:pass@host:port',
                    '--logfile=/tmp/micro/celery/logs/%N.log',
                    '--pidfile=/tmp/micro/celery/pids/%N.pid',
                    'multi', 'start',
                    'worker1@config_hostname',
                    'worker2@config_hostname',
                    'worker3@config_hostname',
                    'worker4@config_hostname',
                    'worker5@config_hostname',
                    'worker6@config_hostname',
                    'worker7@config_hostname',
                    'worker8@config_hostname',
                    'worker9@config_hostname',
                    'worker10@config_hostname']

        app = CeleryApp()
        args = app._CeleryApp__load_args()
        self.assertEqual(args, expected)
