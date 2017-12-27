import os
import sys
import json
from .cli import CLI
from .config import Config


class Params:
    def __init__(self):
        self.__default = {
            "broker_url": "",
            "queue_name": "micro_queue",
            "hostname": "micro",
            "num_workers": 1,
            "log_path": "/var/log",
            "pid_path": "/var/run"
        }
        self.__cli = CLI()
        self.__args = self.__cli.parse_args()
        self.__check_default()
        self.__config = Config()

    def __check_default(self):
        if self.__args.default_params:
            self.__print_default()
            sys.exit(0)

    def __print_default(self):
        print(json.dumps(self.__default, indent=4))

    def __priority_param(self, cli_param, env_var_name, config_key):
        if cli_param:
            return cli_param

        env_var = os.environ.get(env_var_name)
        if env_var:
            return env_var

        if self.__config.key(config_key):
            return self.__config.key(config_key)

        return self.__default[config_key]

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
