import os
import sys
import json
import pkg_resources
from .cli import CLI
from .config import Config

DEFAULT = {
    "plugins_path": "",
    "broker_url": "",
    "queue_name": "",
    "hostname": "micro",
    "num_workers": 1,
    "log_level": "INFO",
    "log_path": "/var/log/micro",
    "celery_log_level": "INFO",
    "celery_log_path": "/var/log/micro/celery",
    "celery_pid_path": "/var/run/micro/celery"
}


class Params:
    def __init__(self):
        self.__cli = CLI()
        self.__args = self.__cli.parse_args()
        self.__check_default()
        self.__check_version()
        self.__config = self.__get_config()
        self.__set_log_env()

    def __check_default(self):
        if self.__args.default_params:
            print(json.dumps(DEFAULT, indent=4))
            sys.exit(0)

    def __check_version(self):
        if self.__args.version:
            print("Micro", pkg_resources.require("Micro")[0].version)
            sys.exit(0)

    def __set_log_env(self):
        os.environ["MICRO_LOG_PATH"] = self.log_path()
        os.environ["MICRO_LOG_FROM"] = self.log_level()

    def __get_config(self):
        path = self.__args.config_file
        if path:
            return Config(path)

        return Config(os.environ.get("MICRO_CONFIG"))

        return None

    def __priority_param(self, cli_param, env_var_name, config_key):
        if cli_param:
            return cli_param

        env_var = os.environ.get(env_var_name)
        if env_var:
            return env_var

        if self.__config.key(config_key):
            return self.__config.key(config_key)

        return DEFAULT[config_key]

    def broker_url(self):
        return self.__priority_param(self.__args.broker_url,
                                     "MICRO_BROKER_URL",
                                     "broker_url")

    def queue_name(self):
        return self.__priority_param(self.__args.queue_name,
                                     "MICRO_QUEUE_NAME",
                                     "queue_name")

    def hostname(self):
        return self.__priority_param(self.__args.hostname,
                                     "MICRO_HOSTNAME",
                                     "hostname")

    def num_workers(self):
        return int(self.__priority_param(self.__args.num_workers,
                                         "MICRO_NUM_WORKERS",
                                         "num_workers"))

    def log_path(self):
        return self.__priority_param(self.__args.log_path,
                                     "MICRO_CELERY_LOG_PATH",
                                     "log_path")

    def pid_path(self):
        return self.__priority_param(self.__args.pid_path,
                                     "MICRO_CELERY_PID_PATH",
                                     "pid_path")
