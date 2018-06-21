import os
import json
from unittest import TestCase
from micro.core.params import Params
from micro.core.params import DEFAULT
from tests.utils.fakestdout import StdoutLock


class TestParams(TestCase):
    def setUp(self):
        self.env_plugin_path = "env_var_plugin_path"
        self.env_broker_url = "env_var_broker_url"
        self.env_queue_name = "env_var_queue_name"
        os.environ["MICRO_PLUGIN_PATH"] = self.env_plugin_path
        os.environ["MICRO_BROKER_URL"] = self.env_broker_url
        os.environ["MICRO_QUEUE_NAME"] = self.env_queue_name

    def tierDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]

    def test_priority(self):
        os.environ["MICRO_HOSTNAME"] = "env_var_hostname"

        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))
        config_file = os.path.join(parent, "resources", "test_config.json")
        os.environ["MICRO_CONFIG"] = config_file

        params = Params()
        params._Params__args = vars(params._Params__cli.parse_args(
            ["-H", "cli_hostname"]
        ))
        params._Params__set_all()
        self.assertEqual(Params.hostname(), "cli_hostname")

        params = Params()
        self.assertEqual(Params.hostname(), "env_var_hostname")

        del os.environ["MICRO_HOSTNAME"]
        params = Params()
        self.assertEqual(Params.hostname(), "config_hostname")

        del os.environ["MICRO_CONFIG"]
        params = Params()
        self.assertEqual(Params.hostname(),
                         DEFAULT["hostname"])

    def test_default_arg(self):
        params = Params()
        params._Params__args = vars(params._Params__cli.parse_args(
            ["--default-params"]
        ))
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                params._Params__check_default()

        self.assertDictEqual(json.loads(lock.stdout), DEFAULT)

    def test_version(self):
        params = Params()
        params._Params__args = vars(params._Params__cli.parse_args(
            ["--version"]
        ))
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                params._Params__check_version()

        self.assertEqual(lock.stdout.split(" ")[0], "Micro")

    def test_all_params(self):
        Params()
        self.assertEqual(Params.plugin_path(), self.env_plugin_path)
        self.assertEqual(Params.broker_url(), self.env_broker_url)
        self.assertEqual(Params.queue_name(), self.env_queue_name)
        self.assertEqual(Params.hostname(), DEFAULT["hostname"])
        self.assertEqual(Params.num_workers(), DEFAULT["num_workers"])
        self.assertEqual(Params.log_level(), DEFAULT["log_level"])
        self.assertEqual(Params.log_path(), DEFAULT["log_path"])
        self.assertEqual(Params.celery_log_level(),
                         DEFAULT["celery_log_level"])
        self.assertEqual(Params.celery_log_path(), DEFAULT["celery_log_path"])
        self.assertEqual(Params.celery_pid_path(), DEFAULT["celery_pid_path"])

    def test_all_types(self):
        Params()
        self.assertEqual(type(Params.plugin_path()), str)
        self.assertEqual(type(Params.broker_url()), str)
        self.assertEqual(type(Params.queue_name()), str)
        self.assertEqual(type(Params.hostname()), str)
        self.assertEqual(type(Params.num_workers()), int)
        self.assertEqual(type(Params.log_level()), str)
        self.assertEqual(type(Params.log_path()), str)
        self.assertEqual(type(Params.celery_log_level()), str)
        self.assertEqual(type(Params.celery_log_path()), str)
        self.assertEqual(type(Params.celery_pid_path()), str)
