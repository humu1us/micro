import os
import logging
from .params import Params
from ..core.utils import set_folder

FILE_NAME = "micro.log"
LOG_FORMAT = "[%(asctime)s] %(levelname)s: " + \
    "%(message)s - %(filename)s, %(funcName)s, %(lineno)s"
LOG_DEBUG_FORMAT = "[%(asctime)s] [%(process)d] %(levelname)s: " + \
    "%(message)s - %(name)s, %(filename)s, %(funcName)s, %(lineno)s"


class Logger():
    def __init__(self):
        self.__path = Params.log_path()
        self.__level = logging.getLevelName(Params.log_level())
        self.__micro_log = Params.namespace()
        self.__celery_log = "celery"
        self.__gunicorn_log = "gunicorn.error"

        set_folder(self.__path)

        self.__micro = logging.getLogger(self.__micro_log)
        self.__micro.setLevel(self.__level)
        self.__celery = logging.getLogger(self.__celery_log)
        self.__celery.setLevel(self.__level)
        self.__gunicorn = logging.getLogger(self.__gunicorn_log)
        self.__gunicorn.setLevel(self.__level)

        datefmt = "%Y-%m-%d %H:%M:%S"
        self.__formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=datefmt)
        if self.__level == logging.DEBUG:
            self.__formatter = logging.Formatter(fmt=LOG_DEBUG_FORMAT,
                                                 datefmt=datefmt)

        if not self.__micro.handlers:
            self.__set_file_handler()

    def __set_file_handler(self):
        handler = logging.FileHandler(os.path.join(self.__path, FILE_NAME))
        handler.setLevel(self.__level)
        handler.setFormatter(self.__formatter)
        self.__micro.addHandler(handler)
        self.__celery.addHandler(handler)
        self.__gunicorn.addHandler(handler)

    def debug(self, message):
        self.__micro.debug(message)

    def info(self, message):
        self.__micro.info(message)

    def warning(self, message):
        self.__micro.warning(message)

    def error(self, message):
        self.__micro.error(message)
