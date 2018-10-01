import json
import os
import shutil
from argparse import ArgumentParser
from unittest import TestCase
from micro import __version__
from micro.core.params import Params
from micro.core.settingbase import SettingBase
from tests.utils.fakestdout import StdoutLock


class TestParams(TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.path.pardir))

        cls.config_file = os.path.join(path, "resources", "test_config.json")
        cls.env_celery = "1"
        cls.env_gunicorn = "1"
        cls.env_plugin_path = "/tmp/micro/env_var_plugin_path"
        cls.env_broker_url = "env_var_broker_url"
        cls.env_task_queues = "env_var_queue_name"
        os.environ["MICRO_CONFIG_FILE"] = cls.config_file
        cls.test_folders = [
            ["MICRO_PLUGIN_PATH", cls.env_plugin_path],
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_params_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_params_pids"]
        ]
        for f in cls.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        del os.environ["MICRO_CONFIG_FILE"]
        del os.environ["MICRO_PLUGIN_PATH"]
        for f in cls.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

    def test_priority(self):
        os.environ["MICRO_TASK_QUEUES"] = self.env_task_queues

        params = Params(setall=True)
        params._Params__args = vars(
            params._Params__cli.parse_args(["-q", "cli_queuename"])
        )
        params.set_params()
        self.assertEqual(Params.task_queues(), "cli_queuename")

        Params(setall=True).set_params()
        self.assertEqual(Params.task_queues(), self.env_task_queues)

        del os.environ["MICRO_TASK_QUEUES"]
        Params(setall=True).set_params()
        self.assertEqual(Params.task_queues(), "queue_name")

        # hostname does not have any value in the config file
        self.assertEqual(Params.hostname(), "micro")

    def test_default_arg(self):
        params = Params(setall=True)
        params._Params__args = vars(params._Params__cli.parse_args(["-d"]))
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                params._Params__check_default()

        defaults = {
            "gunicorn": {
                "bind": "0.0.0.0:8000",
                "workers": 1
            },
            "celery": {
                "broker_url": "",
                "workers": 1,
                "hostname": "micro",
                "task_queues": ""
            },
            "micro": {
                "log_file_name": "micro.log",
                "log_folder_path": "/var/log/micro",
                "log_level": "WARNING",
                "pid_folder_path": "/var/run/micro",
                "plugin_path": ""
            }
        }
        self.assertDictEqual(json.loads(lock.stdout), defaults)

    def test_version(self):
        params = Params(setall=True)
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                params._Params__args = vars(
                    params._Params__cli.parse_args(["-v"])
                )

        version = "setup.py (version %s)" % __version__
        self.assertEqual(lock.stdout.strip(), version)

    def test_no_cli(self):
        class SettingTest(SettingBase):
            name = "name"

        cli = ArgumentParser()
        setting = SettingTest(parse=cli, defaults={})
        self.assertEqual(setting.name, "name")
