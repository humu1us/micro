import os
from unittest import TestCase
from micro.core.config import Config


class TestConfig(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.file = os.path.join(self.parent, "resources", "test_config.json")

    def test_open(self):
        with self.assertRaises(SystemExit) as se:
            Config(self.parent)

        err = "ERROR: config file not found: " + self.parent
        self.assertEqual(se.exception.args[0], err)

    def test_read_keys(self):
        conf = Config(self.file)
        self.assertEqual(conf.key("plugin_path"), "/path/to/plugins/folder")
        self.assertEqual(conf.key("broker_url"), "test://user:pass@host:port")
        self.assertEqual(conf.key("queue_name"), "queue_name")
        self.assertEqual(conf.key("hostname"), "config_hostname")
        self.assertEqual(conf.key("num_workers"), 10)
        self.assertEqual(conf.key("log_level"), "ERROR")
        self.assertEqual(conf.key("log_path"), "/tmp/micro/logs")
        self.assertEqual(conf.key("celery_log_level"), "ERROR")
        self.assertEqual(conf.key("celery_log_path"), "/tmp/micro/celery/logs")
        self.assertEqual(conf.key("celery_pid_path"), "/tmp/micro/celery/pids")
