import logging
import os
import shutil
from unittest import TestCase
from micro.core.settingbase import SettingBase
from micro.core.validate import Validate


class SettingTest(SettingBase):
    name = "s"


class TestValidate(TestCase):
    def test_positive_int(self):
        SettingTest.validator = Validate.positive_int
        s = SettingTest()

        self.assertIsNone(s.validator(None))

        self.assertEqual(s.validator(1), 1)
        self.assertEqual(s.validator(10000000), 10000000)

        for v in ["1", 3.5, -5.8, "a", True, False, [1], {1}, (1,)]:
            with self.assertRaises(SystemExit) as se:
                s.validator(v)
            msg = "[s] must be integer: %s" % str(v)
            self.assertEqual(se.exception.args[0], msg)

        for v in [0, -1, -345]:
            with self.assertRaises(SystemExit) as se:
                s.validator(v)
            msg = "[s] must be positive: %s" % str(v)
            self.assertEqual(se.exception.args[0], msg)

    def test_file_exist(self):
        SettingTest.validator = Validate.file_exist
        s = SettingTest()

        self.assertIsNone(s.validator(None))

        value = "/path/to/fake/file"
        with self.assertRaises(SystemExit) as se:
            s.validator(value)
        msg = "[s] file does not exists: %s" % str(value)
        self.assertEqual(se.exception.args[0], msg)

        value = os.path.abspath(os.path.dirname(__file__))
        with self.assertRaises(SystemExit) as se:
            s.validator(value)
        msg = "[s] path is not a valid file: %s" % str(value)
        self.assertEqual(se.exception.args[0], msg)

        value = os.path.abspath(__file__)
        self.assertEqual(s.validator(value), value)

    def test_folder_exist(self):
        SettingTest.validator = Validate.folder_exist
        s = SettingTest()

        self.assertIsNone(s.validator(None))

        value = os.path.abspath(__file__)
        with self.assertRaises(SystemExit) as se:
            s.validator(value)
        msg = "[s] path name a file instead a folder: %s" % str(value)
        self.assertEqual(se.exception.args[0], msg)

        value = "/path/to/fake/folder"
        with self.assertRaises(SystemExit) as se:
            s.validator(value)
        msg = "[s] directory does not exists: %s" % str(value)
        self.assertEqual(se.exception.args[0], msg)

        value = "/tmp/micro/test_creation_folder"
        s.validator(value)
        self.assertEqual(value, value)
        shutil.rmtree(value)

        value = os.path.abspath(os.path.dirname(__file__))
        self.assertEqual(s.validator(value), value)

    def test_bool(self):
        SettingTest.validator = Validate.bool
        s = SettingTest()

        self.assertIsNone(s.validator(None))

        for v in [1, 100, 0, "true", "false"]:
            with self.assertRaises(SystemExit) as se:
                s.validator(v)
            msg = "[s] must be bool: %s" % str(v)
            self.assertEqual(se.exception.args[0], msg)

        self.assertTrue(s.validator(True))
        self.assertFalse(s.validator(False))

    def test_log_level(self):
        SettingTest.validator = Validate.log_level
        s = SettingTest()

        self.assertIsNone(s.validator(None))

        levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARN,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
            logging.FATAL
        ]
        for v in levels:
            self.assertEqual(s.validator(v), v)

        levels = [
            "DEBUG",
            "INFO",
            "WARN",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "FATAL"
        ]
        for v in levels:
            self.assertEqual(s.validator(v), v)

        for v in ["a", "info", 1, ["INFO"], {"INFO"}, ("INFO",)]:
            with self.assertRaises(SystemExit) as se:
                s.validator(v)
            msg = "[s] log level not valid: %s" % str(v)
            self.assertEqual(se.exception.args[0], msg)
