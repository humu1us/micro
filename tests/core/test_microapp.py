from unittest import TestCase
from micro.core.microapp import MicroApp
import os


class TestMicroApp(TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.path.pardir))

        path = os.path.join(path, "resources", "test_config.json")
        os.environ["MICRO_CONFIG"] = path

    def test_load_args(self):
        expected = ['celery',
                    '-A', 'micro.api.endpoints',
                    '-Q', 'queue_name',
                    '-l', 'ERROR',
                    '-b', 'test://user:pass@host:port//',
                    '--logfile=/path/to/logs/%N.log',
                    '--pidfile=/path/to/pids/%N.pid',
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

        app = MicroApp()
        args = app._MicroApp__load_args()
        self.assertEqual(args, expected)
