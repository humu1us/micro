import os
from unittest import TestCase
from micro.core.params import Params


class TestParams(TestCase):
    def test_priority(self):
        os.environ["MICRO_HOSTNAME"] = "env_var_hostname"
        self.__set_config_env()

        params = Params()
        params._Params__args = params._Params__cli.parse_args(
            ["-H", "cli_hostname"])
        self.assertEqual(params.hostname(), "cli_hostname")

        params = Params()
        self.assertEqual(params.hostname(), "env_var_hostname")

        del os.environ["MICRO_HOSTNAME"]
        params = Params()
        self.assertEqual(params.hostname(), "config_hostname")

        del os.environ["MICRO_CONFIG"]
        params = Params()
        self.assertEqual(params.hostname(),
                         params._Params__default["hostname"])

    def __set_config_env(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.file = os.path.join(self.parent, "test_config.json")
        os.environ["MICRO_CONFIG"] = self.file
