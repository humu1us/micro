from os import path
from os import environ
from unittest import TestCase
from micro.core.config import Config


class TestConfig(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = path.abspath(path.join(path.dirname(__file__),
                                             path.pardir))
        self.file = path.join(self.parent, "test_config.json")
        environ["MICRO_CONFIG"] = self.file
        self.config = Config()

    def test_open(self):
        environ["MICRO_CONFIG"] = self.parent
        with self.assertRaises(Exception) as context:
            Config()
        self.assertEqual(type(context.exception), IsADirectoryError)

        environ["MICRO_CONFIG"] = path.join(self.parent, "wrong_name.json")
        with self.assertRaises(Exception) as context:
            Config()
        self.assertEqual(type(context.exception), FileNotFoundError)

    def test_read_keys(self):
        self.assertEqual(self.config.key("plugin_path"),
                         "/path/to/plugins/folder"),
        self.assertEqual(self.config.key("broker_url"),
                         "test://user:pass@host:port//")
        self.assertEqual(self.config.key("queue_name"), "queue name")
        self.assertEqual(self.config.key("hostname"), "test-host")
        self.assertEqual(self.config.key("num_workers"), 10)
        self.assertEqual(self.config.key("log_from"), "ERROR")
        self.assertEqual(self.config.key("log_path"), "/path/to/logs")
        self.assertEqual(self.config.key("pid_path"), "/path/to/pids")
