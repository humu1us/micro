import os
import json
from unittest import TestCase
from micro import __version__
from micro.core.config import Config
from micro.core.params import Params
from micro.core.params import DEFAULT
from tests.utils.fakestdout import StdoutLock


class TestParams(TestCase):
    def setUp(self):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))
        self.config_file = os.path.join(parent,
                                        "resources",
                                        "test_config.json")
        self.env_plugin_path = "env_var_plugin_path"
        self.env_broker_url = "env_var_broker_url"
        self.env_queue_name = "env_var_queue_name"
        self.env_celery = "1"
        self.env_api_rest = "1"
        os.environ["MICRO_PLUGIN_PATH"] = self.env_plugin_path
        os.environ["MICRO_BROKER_URL"] = self.env_broker_url
        os.environ["MICRO_QUEUE_NAME"] = self.env_queue_name
        os.environ["MICRO_CELERY"] = self.env_celery
        os.environ["MICRO_API_REST"] = self.env_api_rest

    def tierDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_CELERY"]
        del os.environ["MICRO_API_REST"]

    def test_priority(self):
        os.environ["MICRO_HOSTNAME"] = "env_var_hostname"

        os.environ["MICRO_CONFIG"] = self.config_file

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

        self.assertEqual(lock.stdout.split(" ")[1], __version__)

    def test_required(self):
        params = Params()
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                params._Params__args = vars(params._Params__cli.parse_args(
                    ["--help"]
                ))
        micro_help = lock.stdout

        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["_MICRO_QUEUE_NAME"]
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                Params()

        self.assertEqual(lock.stdout, micro_help)

        os.environ["MICRO_QUEUE_NAME"] = self.env_queue_name
        Params()
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["_MICRO_BROKER_URL"]
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                Params()

        self.assertEqual(lock.stdout, micro_help)

        os.environ["MICRO_BROKER_URL"] = self.env_broker_url
        Params()
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["_MICRO_PLUGIN_PATH"]
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                Params()

        self.assertEqual(lock.stdout, micro_help)

        os.environ["MICRO_PLUGIN_PATH"] = self.env_plugin_path
        Params()
        del os.environ["MICRO_CELERY"]
        del os.environ["_MICRO_CELERY"]
        del os.environ["MICRO_API_REST"]
        del os.environ["_MICRO_API_REST"]
        with self.assertRaises(SystemExit) as mmg:
            Params()

        error = "neither Celery nor API Rest has been selected"
        self.assertEqual(str(mmg.exception), error)

        os.environ["MICRO_CELERY"] = self.env_celery
        os.environ["MICRO_API_REST"] = self.env_api_rest

    def test_get_config(self):
        params = Params()
        params._Params__args = vars(params._Params__cli.parse_args(
            ["-c", self.config_file]
        ))
        fake_path = "/fake/path/to/config.json"
        os.environ["MICRO_CONFIG"] = fake_path
        config = params._Params__get_config()
        self.assertTrue(isinstance(config, Config))

        with self.assertRaises(SystemExit) as se:
            Params()

        err = "ERROR: config file not found: "
        err += fake_path
        self.assertEqual(se.exception.args[0], err)

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
        self.assertEqual(Params.celery(), self.env_celery)
        self.assertEqual(Params.api_rest(), self.env_api_rest)

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
        self.assertEqual(type(Params.celery()), str)
        self.assertEqual(type(Params.api_rest()), str)
