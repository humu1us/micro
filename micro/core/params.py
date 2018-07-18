import os
import sys
import json
from .cli import CLI
from .config import Config
from .. import __version__

PLUGIN_PATH = 0
BROKER_URL = 1
QUEUE_NAME = 2
HOSTNAME = 3
NUM_WORKERS = 4
LOG_LEVEL = 5
LOG_PATH = 6
CELERY_LOG_LEVEL = 7
CELERY_LOG_PATH = 8
CELERY_PID_PATH = 9
CELERY = 10
GUNICORN = 11
BIND = 12

PARAMS = {
    PLUGIN_PATH: {"var": "plugin_path",
                  "env": "MICRO_PLUGIN_PATH"},
    BROKER_URL: {"var": "broker_url",
                 "env": "MICRO_BROKER_URL"},
    QUEUE_NAME: {"var": "queue_name",
                 "env": "MICRO_QUEUE_NAME"},
    HOSTNAME: {"var": "hostname",
               "env": "MICRO_HOSTNAME"},
    NUM_WORKERS: {"var": "num_workers",
                  "env": "MICRO_NUM_WORKERS"},
    LOG_LEVEL: {"var": "log_level",
                "env": "MICRO_LOG_LEVEL"},
    LOG_PATH: {"var": "log_path",
               "env": "MICRO_LOG_PATH"},
    CELERY_LOG_LEVEL: {"var": "celery_log_level",
                       "env": "MICRO_CELERY_LOG_LEVEL"},
    CELERY_LOG_PATH: {"var": "celery_log_path",
                      "env": "MICRO_CELERY_LOG_PATH"},
    CELERY_PID_PATH: {"var": "celery_pid_path",
                      "env": "MICRO_CELERY_PID_PATH"},
    CELERY: {"var": "celery",
             "env": "MICRO_CELERY"},
    GUNICORN: {"var": "gunicorn",
               "env": "MICRO_GUNICORN"},
    BIND: {"var": "bind",
           "env": "MICRO_GUNICORN_BIND"},
}

DEFAULT = {
    "plugin_path": "",
    "broker_url": "",
    "queue_name": "",
    "hostname": "micro",
    "num_workers": 1,
    "bind": "0.0.0.0:8000",
    "log_level": "INFO",
    "log_path": "/var/log/micro",
    "celery_log_level": "INFO",
    "celery_log_path": "/var/log/micro/celery",
    "celery_pid_path": "/var/run/micro/celery"
}


class Params:
    def __init__(self):
        self.__cli = CLI()
        self.__args = vars(self.__cli.parse_args())
        self.__check_default()
        self.__check_version()
        self.__config = self.__get_config()
        self.__set_all()
        self.__check_required()

    def __check_default(self):
        if self.__args.get("default_params"):
            print(json.dumps(DEFAULT, indent=4))
            sys.exit(0)

    def __check_version(self):
        if self.__args.get("version"):
            here = os.path.abspath(__file__)
            pkg_path = os.path.dirname(os.path.dirname(os.path.dirname(here)))
            print("Micro", __version__, "from", pkg_path)
            sys.exit(0)

    def __get_config(self):
        path = self.__args.get("config_file")
        if path:
            return Config(path)

        return Config(os.environ.get("MICRO_CONFIG"))

    def __priority_param(self, cli_param, env_var_name, config_key):
        if cli_param:
            return cli_param

        env_var = os.environ.get(env_var_name)
        if env_var:
            return env_var

        if self.__config.key(config_key):
            return self.__config.key(config_key)

        return DEFAULT.get(config_key)

    def __set_all(self):
        for p in PARAMS:
            value = self.__priority_param(self.__args.get(PARAMS[p]["var"]),
                                          PARAMS[p]["env"],
                                          PARAMS[p]["var"])
            if value:
                envvar = "_" + PARAMS[p]["env"]
                os.environ[envvar] = str(value)

    def __check_required(self):
        if not Params.plugin_path():
            sys.exit(self.__cli.print_help())

        if Params.celery() and not Params.broker_url():
            sys.exit(self.__cli.print_help())

        if Params.celery() and not Params.queue_name():
            sys.exit(self.__cli.print_help())

        if not Params.celery() and not Params.gunicorn():
            sys.exit("neither Celery nor Gunicorn have been selected")

    @staticmethod
    def namespace():
        return "Micro"

    @staticmethod
    def plugin_path():
        return os.environ.get("_" + PARAMS[PLUGIN_PATH]["env"])

    @staticmethod
    def broker_url():
        return os.environ.get("_" + PARAMS[BROKER_URL]["env"])

    @staticmethod
    def queue_name():
        return os.environ.get("_" + PARAMS[QUEUE_NAME]["env"])

    @staticmethod
    def hostname():
        return os.environ.get("_" + PARAMS[HOSTNAME]["env"])

    @staticmethod
    def num_workers():
        return int(os.environ.get("_" + PARAMS[NUM_WORKERS]["env"]))

    @staticmethod
    def log_level():
        return os.environ.get("_" + PARAMS[LOG_LEVEL]["env"])

    @staticmethod
    def log_path():
        return os.environ.get("_" + PARAMS[LOG_PATH]["env"])

    @staticmethod
    def celery_log_level():
        return os.environ.get("_" + PARAMS[CELERY_LOG_LEVEL]["env"])

    @staticmethod
    def celery_log_path():
        return os.environ.get("_" + PARAMS[CELERY_LOG_PATH]["env"])

    @staticmethod
    def celery_pid_path():
        return os.environ.get("_" + PARAMS[CELERY_PID_PATH]["env"])

    @staticmethod
    def celery():
        return os.environ.get("_" + PARAMS[CELERY]["env"])

    @staticmethod
    def gunicorn():
        return os.environ.get("_" + PARAMS[GUNICORN]["env"])

    @staticmethod
    def bind():
        return os.environ.get("_" + PARAMS[BIND]["env"])
