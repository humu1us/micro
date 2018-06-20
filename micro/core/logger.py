import os
import logging
from .params import Params

log_from = Params.log_level()
log_path = Params.log_path()

log_level = logging.getLevelName(log_from)
logging.getLogger("celery").setLevel(log_level)

log = logging.getLogger()
log.setLevel(log_level)

log_file = os.path.join(log_path, "micro.log")
logger_handler = logging.FileHandler(log_file)
logger_handler.setLevel(log_level)

logfmt = "[%(asctime)s] %(levelname)s: %(message)s - " + \
    "%(filename)s, %(funcName)s, %(lineno)s"

logger_formatter = logging.Formatter(fmt=logfmt,
                                     datefmt="%Y-%m-%d %H:%M:%S")

logger_handler.setFormatter(logger_formatter)

log.addHandler(logger_handler)
