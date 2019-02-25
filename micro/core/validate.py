import logging
import os
import sys


class Validate:
    def positive_int(self, value):
        if value is None:
            return None
        if not isinstance(value, int) or isinstance(value, bool):
            sys.exit("[%s] must be integer: %s" % (self.name, value))
        if value < 1:
            sys.exit("[%s] must be positive: %s" % (self.name, value))
        return value

    def file_exist(self, value):
        if value is None:
            return None
        if not os.path.exists(value):
            sys.exit("[%s] file does not exists: %s" % (self.name, value))
        if not os.path.isfile(value):
            sys.exit("[%s] path is not a valid file: %s" % (self.name, value))
        return value

    def folder_exist(self, value):
        if value is None:
            return None
        if os.path.isfile(value):
            msg = "[%s] path name a file instead a folder: %s" % (self.name,
                                                                  value)
            sys.exit(msg)
        if not os.path.exists(value) or not os.path.isdir(value):
            try:
                os.makedirs(value)
            except Exception:
                msg = "[%s] directory does not exists: %s" % (self.name, value)
                sys.exit(msg)
        return value

    def bool(self, value):
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        sys.exit("[%s] must be bool: %s" % (self.name, value))

    def log_level(self, value):
        levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARN,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
            logging.FATAL
        ]
        if value is None:
            return None
        if isinstance(value, int) and value in levels:
            return value
        if isinstance(value, str) and logging.getLevelName(value) in levels:
            return value
        sys.exit("[%s] log level not valid: %s" % (self.name, value))
