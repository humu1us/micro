import json
import os
import shutil
from unittest import TestCase
from flask import Flask
from micro.core.params import Params


class TestAPIRestEndpoints(TestCase):
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
        from micro.api.apirest import endpoints
        cls.app = Flask("micro_test")
        cls.app.register_blueprint(endpoints)

    @classmethod
    def tearDownClass(cls):
        for f in cls.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

    def test_plugins_api(self):
        resp = [{
            "name": "Example Plugin",
            "version": None,
            "description": "A very simple example plugin"
        }]
        with self.app.test_client() as client:
            response = client.get("/plugins")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertEquals(json.loads(response.data), resp)

    def test_info(self):
        resp = {"error": "plugin not found"}
        with self.app.test_client() as client:
            response = client.get("/info/not-existent-plugin")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertEquals(json.loads(response.data), resp)

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
        with self.app.test_client() as client:
            response = client.get("/info/Example%20Plugin")
            self.assertTrue(True)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertEquals(json.loads(response.data), resp)

    def test_help(self):
        resp = {"error": "plugin not found"}
        with self.app.test_client() as client:
            response = client.get("/help/not-existent-plugin")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertEquals(json.loads(response.data), resp)

        resp = {
            "name": "Example Plugin",
            "version": None,
            "help": "Params: name type string; A name to greet"
        }
        with self.app.test_client() as client:
            response = client.get("/help/Example%20Plugin")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertEquals(json.loads(response.data), resp)

    def test_run(self):
        data = {"wrong_arg": "World"}
        resp = {"error": "plugin not found"}
        with self.app.test_client() as client:
            response = client.post("/run/not-existent-plugin",
                                   data=json.dumps(data),
                                   content_type="application/json")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertEquals(json.loads(response.data), resp)

        resp = {
            "error": "run() got an unexpected keyword argument 'wrong_arg'"
        }
        with self.app.test_client() as client:
            response = client.post("/run/Example%20Plugin",
                                   data=json.dumps(data),
                                   content_type="application/json")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertEquals(json.loads(response.data), resp)

        data = {"name": "World"}
        with self.app.test_client() as client:
            response = client.post("/run/Example%20Plugin",
                                   data=json.dumps(data),
                                   content_type="application/json")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.mimetype, "application/json")
            self.assertDictEqual(json.loads(response.data),
                                 {"msg": "Hello World!!!"})
