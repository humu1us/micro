import os
import logging

log_path = os.environ.get("_MICRO_LOG_PATH")
log_from = os.environ.get("_MICRO_LOG_FROM")
if not log_path:
    raise RuntimeError("log path not set")
if not log_from:
    raise RuntimeError("log level from not set")

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
