import json
import os
import shutil
from unittest import TestCase
from micro.core.params import Params


class TestCeleryEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))
        plugins = os.path.join(parent, "resources", "plugin")
        os.environ["MICRO_PLUGIN_PATH"] = plugins
        cls.test_folders = [
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_apirest_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_apirest_pids"]
        ]
        for f in cls.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

        Params(setall=True).set_params()

    @classmethod
    def tearDownClass(cls):
        for f in cls.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

    def test_plugins(self):
        from micro.api.celery import plugins
        resp = [{
            "name": "Example Plugin",
            "version": None,
            "description": "A very simple example plugin"
        }]
        self.assertEqual(plugins.apply().get(), json.dumps(resp))

    def test_info(self):
        from micro.api.celery import info
        long_description = "This plugin is a very simple example, " + \
                           "for that reason, we don't have a long description"
        resp = {
            "name": "Example Plugin",
            "version": None,
            "url": None,
            "author": "Jhon Doe",
            "author_email": None,
            "description": "A very simple example plugin",
            "long_description": long_description
        }
        self.assertEqual(info.apply(args=("Example Plugin",)).get(),
                         json.dumps(resp))

        self.assertEqual(info.apply(args=("Non-existent plugin",)).get(),
                         json.dumps({"error": "plugin not found"}))

    def test_help(self):
        from micro.api.celery import help
        resp = {
            "name": "Example Plugin",
            "version": None,
            "help": "Params: name type string; A name to greet"
        }
        self.assertEqual(help.apply(args=("Example Plugin",)).get(),
                         json.dumps(resp))

        self.assertEqual(help.apply(args=("Non-existent plugin",)).get(),
                         json.dumps({"error": "plugin not found"}))

    def test_run(self):
        from micro.api.celery import run
        self.assertEqual(run.apply(args=("Example Plugin",),
                                   kwargs={"name": "World"}).get(),
                         json.dumps({"msg": "Hello World!!!"}))

        error = "run() got an unexpected keyword argument \'wrong_arg\'"
        self.assertEqual(run.apply(args=("Example Plugin",),
                                   kwargs={"wrong_arg": "World"}).get(),
                         json.dumps({"error": error}))

        self.assertEqual(run.apply(args=("Non-existent plugin",),
                                   kwargs={"wrong_name": "World"}).get(),
                         json.dumps({"error": "plugin not found"}))
