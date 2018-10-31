import os
import shutil
from unittest import TestCase
from testfixtures import LogCapture
from micro.core.logger import Logger
from micro.core.params import Params


class TestLogger(TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.path.pardir))

        path = os.path.join(path, "resources", "test_config.json")
        os.environ["MICRO_CONFIG_FILE"] = path
        cls.test_folders = [
            ["MICRO_PLUGIN_PATH", "/tmp/micro_logger_plugin"],
            ["MICRO_LOG_FOLDER_PATH", "/tmp/micro_logger_logs"],
            ["MICRO_PID_FOLDER_PATH", "/tmp/micro_logger_pids"]
        ]
        for f in cls.test_folders:
            os.environ[f[0]] = f[1]
            os.makedirs(f[1], exist_ok=True)

        Params(setall=True).set_params()

    @classmethod
    def tearDownClass(cls):
        del os.environ["MICRO_CONFIG_FILE"]
        for f in cls.test_folders:
            del os.environ[f[0]]
            shutil.rmtree(f[1])

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
