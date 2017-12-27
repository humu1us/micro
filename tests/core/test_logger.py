import os
from unittest import TestCase


class TestPluginManager(TestCase):
    def tearDown(self):
        del os.environ["MICRO_LOG_PATH"]

    def test_contructor(self):
        with self.assertRaises(Exception) as context:
            from micro.core.logger import log
        self.assertEqual(type(context.exception), RuntimeError)

        os.environ["MICRO_LOG_PATH"] = "/"

        with self.assertRaises(Exception) as context:
            from micro.core.logger import log
        self.assertEqual(type(context.exception), RuntimeError)
