import os
import logging

log_path = os.environ.get("MICRO_LOG_PATH")
if not log_path:
    raise RuntimeError("MICRO_LOG_PATH not set")

logging.getLogger("celery").setLevel(logging.INFO)

log = logging.getLogger()
log.setLevel(logging.INFO)

log_file = os.path.join(log_path, "micro.log")
logger_handler = logging.FileHandler(log_file)
logger_handler.setLevel(logging.INFO)

logfmt = "[%(asctime)s] %(levelname)s: %(message)s - " + \
    "%(filename)s, %(funcName)s, %(lineno)s"

logger_formatter = logging.Formatter(fmt=logfmt,
                                     datefmt="%Y-%m-%d %H:%M:%S")

logger_handler.setFormatter(logger_formatter)

log.addHandler(logger_handler)
