import os
import logging
from .params import Params
from ..core.utils import set_folder

LOG_FORMAT = "[%(asctime)s] %(levelname)s: " + \
    "%(message)s - %(filename)s, %(funcName)s, %(lineno)s"


class Logger():
    def __init__(self):
        self.__path = Params.log_path()
        self.__level = Params.log_level()
        self.__celery_level = Params.celery_log_level()
        self.__formatter = logging.Formatter(fmt=LOG_FORMAT,
                                             datefmt="%Y-%m-%d %H:%M:%S")

        set_folder(self.__path)
        self.celery = logging.getLogger("celery")
        self.celery.setLevel(self.__celery_level)
        self.micro = logging.getLogger("Micro")
        self.micro.setLevel(self.__level)

        if not self.micro.handlers:
            self.__set_file_handler()

    def __set_file_handler(self):
        handler = logging.FileHandler(os.path.join(self.__path, "micro.log"))
        handler.setLevel(self.__level)
        handler.setFormatter(self.__formatter)
        self.micro.addHandler(handler)
        self.celery.addHandler(handler)

    def debug(self, message):
        self.micro.debug(message)

    def info(self, message):
        self.micro.info(message)

    def warning(self, message):
        self.micro.warning(message)

    def error(self, message):
        self.micro.error(message)
