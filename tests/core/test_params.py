from os import path
from os import environ
from unittest import TestCase
from micro.core.params import Params


class TestParams(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = path.abspath(path.join(path.dirname(__file__),
                                             path.pardir))
        self.file = path.join(self.parent, "test_config.json")
        environ["MICRO_CONFIG"] = self.file

        environ["MICRO_HOSTNAME"] = "env_var_hostname"

    def test_priority(self):
        params = Params()
        self.assertEqual(params.hostname(), "env_var_hostname")

        del environ["MICRO_HOSTNAME"]
        params = Params()
        self.assertEqual(params.hostname(), "config_hostname")

        del environ["MICRO_CONFIG"]
        params = Params()
        self.assertEqual(params.hostname(), "micro")
