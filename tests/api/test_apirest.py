import os
import json
from unittest import TestCase
from flask import Flask
from micro.core.params import Params


class TestAPIRestEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  os.path.pardir))
        cls.path = os.path.join(cls.parent, "resources", "plugin")
        os.environ["MICRO_PLUGIN_PATH"] = cls.path
        os.environ["MICRO_BROKER_URL"] = "broker_test"
        os.environ["MICRO_QUEUE_NAME"] = "queue_test"
        os.environ["MICRO_LOG_PATH"] = cls.parent
        os.environ["MICRO_LOG_FROM"] = "INFO"
        os.environ["MICRO_CELERY"] = "1"
        Params()
        from micro.api.apirest import endpoints
        cls.app = Flask("micro_test")
        cls.app.register_blueprint(endpoints)

    @classmethod
    def tearDownClass(cls):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_LOG_FROM"]
        del os.environ["MICRO_CELERY"]

    def test_plugins(self):
        resp = [{
            "name": "Example Plugin",
            "version": None,
            "description": "A very simple example plugin"
        }]
        with self.app.test_client() as client:
            response = client.get("/plugins")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(json.loads(response.data), resp)

    def test_info(self):
        resp = {"error": "plugin not found"}
        with self.app.test_client() as client:
            response = client.get("/info/not-existent-plugin")
            self.assertEquals(response.status_code, 200)
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
            self.assertEquals(response.status_code, 200)
            self.assertEquals(json.loads(response.data), resp)

    def test_help(self):
        resp = {"error": "plugin not found"}
        with self.app.test_client() as client:
            response = client.get("/help/not-existent-plugin")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(json.loads(response.data), resp)

        resp = {
            "name": "Example Plugin",
            "version": None,
            "help": "Params: name type string; A name to greet"
        }
        with self.app.test_client() as client:
            response = client.get("/help/Example%20Plugin")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(json.loads(response.data), resp)

    def test_run(self):
        data = {"wrong_arg": "World"}
        resp = {"error": "plugin not found"}
        with self.app.test_client() as client:
            response = client.post("/run/not-existent-plugin",
                                   data=json.dumps(data),
                                   content_type="application/json")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(json.loads(response.data), resp)

        resp = {
            "error": "run() got an unexpected keyword argument 'wrong_arg'"
        }
        with self.app.test_client() as client:
            response = client.post("/run/Example%20Plugin",
                                   data=json.dumps(data),
                                   content_type="application/json")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(json.loads(response.data), resp)

        data = {"name": "World"}
        with self.app.test_client() as client:
            response = client.post("/run/Example%20Plugin",
                                   data=json.dumps(data),
                                   content_type="application/json")
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.data.decode("utf-8"), "Hello World!!!")
