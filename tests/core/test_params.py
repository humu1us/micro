import os
import io
import sys
import json
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

    def test_default_arg(self):
        stdout = sys.stdout
        sys.stdout = io.StringIO()

        params = Params()
        params._Params__args = params._Params__cli.parse_args(
            ["--default-params"])
        with self.assertRaises(SystemExit):
            params._Params__check_default()

        output = sys.stdout.getvalue()
        sys.stdout = stdout
        self.assertDictEqual(json.loads(output), params._Params__default)

    def test_all_params(self):
        del os.environ["MICRO_CONFIG"]
        params = Params()
        self.assertEqual(params.broker_url(),
                         params._Params__default["broker_url"])
        self.assertEqual(params.queue_name(),
                         params._Params__default["queue_name"])
        self.assertEqual(params.hostname(),
                         params._Params__default["hostname"])
        self.assertEqual(params.num_workers(),
                         params._Params__default["num_workers"])
        self.assertEqual(params.log_from(),
                         params._Params__default["log_from"])
        self.assertEqual(params.log_path(),
                         params._Params__default["log_path"])
        self.assertEqual(params.pid_path(),
                         params._Params__default["pid_path"])

    def __set_config_env(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.file = os.path.join(self.parent, "test_config.json")
        os.environ["MICRO_CONFIG"] = self.file
