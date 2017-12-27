import os
from unittest import TestCase
from micro.core.config import Config


class TestConfig(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.file = os.path.join(self.parent, "resources", "test_config.json")
        os.environ["MICRO_CONFIG"] = self.file
        self.config = Config()

    def tearDown(self):
        del os.environ["MICRO_CONFIG"]

    def test_open(self):
        os.environ["MICRO_CONFIG"] = self.parent
        with self.assertRaises(Exception) as context:
            Config()
        self.assertEqual(type(context.exception), IsADirectoryError)

        os.environ["MICRO_CONFIG"] = os.path.join(self.parent, "fakeconf.json")
        with self.assertRaises(Exception) as context:
            Config()
        self.assertEqual(type(context.exception), FileNotFoundError)

    def test_read_keys(self):
        self.assertEqual(self.config.key("plugin_path"),
                         "/path/to/plugins/folder"),
        self.assertEqual(self.config.key("broker_url"),
                         "test://user:pass@host:port//")
        self.assertEqual(self.config.key("queue_name"), "queue_name")
        self.assertEqual(self.config.key("hostname"), "config_hostname")
        self.assertEqual(self.config.key("num_workers"), 10)
        self.assertEqual(self.config.key("log_path"), "/path/to/logs")
        self.assertEqual(self.config.key("pid_path"), "/path/to/pids")
