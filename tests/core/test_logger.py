import os
from unittest import TestCase
from testfixtures import LogCapture
from micro.core.logger import Logger
from micro.core.params import Params


class TestConfig(TestCase):
    def setUp(self):
        self.parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        self.file = os.path.join(self.parent, "resources", "test_config.json")
        os.environ["MICRO_PLUGIN_PATH"] = "plugin_path_test"
        os.environ["MICRO_BROKER_URL"] = "broker_test"
        os.environ["MICRO_QUEUE_NAME"] = "queue_test"
        os.environ["MICRO_LOG_PATH"] = self.parent
        os.environ["MICRO_LOG_LEVEL"] = "DEBUG"
        os.environ["MICRO_CELERY"] = "1"
        Params()

    def tearDown(self):
        del os.environ["MICRO_PLUGIN_PATH"]
        del os.environ["MICRO_BROKER_URL"]
        del os.environ["MICRO_QUEUE_NAME"]
        del os.environ["MICRO_LOG_PATH"]
        del os.environ["MICRO_LOG_LEVEL"]
        del os.environ["MICRO_CELERY"]

    def test_debug(self):
        log = Logger()
        msg = "debug test message"
        with LogCapture("Micro") as logs:
            log.debug(msg)
        logs.check(("Micro", "DEBUG", msg))

    def test_info(self):
        log = Logger()
        msg = "info test message"
        with LogCapture("Micro") as logs:
            log.info(msg)
        logs.check(("Micro", "INFO", msg))

    def test_warning(self):
        log = Logger()
        msg = "warning test message"
        with LogCapture("Micro") as logs:
            log.warning(msg)
        logs.check(("Micro", "WARNING", msg))

    def test_error(self):
        log = Logger()
        msg = "error test message"
        with LogCapture("Micro") as logs:
            log.error(msg)
        logs.check(("Micro", "ERROR", msg))
