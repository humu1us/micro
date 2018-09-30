import os
import shutil
from unittest import TestCase
from flask import Flask
from micro.core.params import Params


class TestGunicornApp(TestCase):
    @classmethod
    def setUpClass(cls):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))

        config = os.path.join(parent, "resources", "test_config.json")
        plugins = os.path.join(parent, "resources", "plugin")
        os.environ["MICRO_CONFIG_FILE"] = config
        os.environ["MICRO_PLUGIN_PATH"] = plugins
        os.environ["MICRO_GUNICORN"] = "1"
        cls.test_folders = [
            ["MICRO_PLUGIN_PATH", "/tmp/micro_gunicornapp_plugin"],
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_gunicornapp_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_gunicornapp_pids"]
        ]
        for f in cls.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

        Params(setall=True).set_params()

    @classmethod
    def tearDownClass(cls):
        del os.environ["MICRO_CONFIG_FILE"]
        del os.environ["MICRO_GUNICORN"]
        for f in cls.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

    def test_load_config(self):
        from micro.core.gunicornapp import GunicornApp
        app = GunicornApp()
        app.load_config()
        self.assertEqual(app.cfg.bind[0], "localhost:5050")
        self.assertEqual(app.cfg.workers, 8)
        self.assertTrue(app.cfg.daemon)

    def test_load(self):
        from micro.core.gunicornapp import GunicornApp
        app = GunicornApp()
        flask_app = app.load()
        self.assertTrue(isinstance(flask_app, Flask))
