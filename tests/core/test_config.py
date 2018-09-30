import os
from unittest import TestCase
from micro.core.config import Config


class TestConfig(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  os.path.pardir))
        cls.file = os.path.join(cls.parent, "resources", "test_config.json")

    def test_open(self):
        with self.assertRaises(Exception) as ctx:
            Config(path=self.parent)
        self.assertEqual(type(ctx.exception), IsADirectoryError)

    def test_read_keys(self):
        conf = Config(path=self.file)
        self.assertEqual(conf.key("micro", "plugin_path"),
                         "/tmp/micro/plugins")
        self.assertEqual(conf.key("micro", "log_level"), "ERROR")
        self.assertEqual(conf.key("micro", "log_folder_path"),
                         "/tmp/micro/logs")
        self.assertEqual(conf.key("micro", "log_file_name"), "micro_test.log")
        self.assertEqual(conf.key("micro", "pid_folder_path"),
                         "/tmp/micro/pids")
        self.assertEqual(conf.key("celery", "broker_url"),
                         "test://user:pass@host:port")
        self.assertEqual(conf.key("celery", "task_queues"),
                         "queue_name")
        self.assertEqual(conf.key("celery", "workers"), 10)
        self.assertEqual(conf.key("gunicorn", "bind"), "localhost:5050")
        self.assertEqual(conf.key("gunicorn", "workers"), 8)
