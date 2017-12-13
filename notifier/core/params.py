import os
import sys
import json
from .cli import CLI
from .config import Config


class Params:
    def __init__(self):
        self.__default = {
            "plugin_path": "/etc/notifier/plugins",
            "broker_url": "",
            "queue_name": "notifier_queue",
            "hostname": "notifier",
            "num_workers": 1,
            "log_from": "INFO",
            "log_path": "/var/logs",
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

    def plugin_path(self):
        if self.__args.plugin_path:
            return self.__args.plugin_path

        plugin_path_os = os.environ.get("NOTIFIER_PLUGIN_PATH")
        if plugin_path_os:
            return plugin_path_os

        if self.__config.key("plugin_path"):
            return self.__config.key("plugin_path")

        return self.__default["plugin_path"]

    def broker_url(self):
        if self.__args.broker_url:
            return self.__args.broker_url

        broker_url_os = os.environ.get("NOTIFIER_BROKER_URL")
        if broker_url_os:
            return broker_url_os

        if self.__config.key("broker_url"):
            return self.__config.key("broker_url")

        return None

    def queue_name(self):
        if self.__args.queue_name:
            return self.__args.queue_name

        queue_name_os = os.environ.get("NOTIFIER_QUEUE_NAME")
        if queue_name_os:
            return queue_name_os

        if self.__config.key("queue_name"):
            return self.__config.key("queue_name")

        return self.__default["queue_name"]

    def hostname(self):
        if self.__args.hostname:
            return self.__args.hostname

        hostname_os = os.environ.get("NOTIFIER_HOSTNAME")
        if hostname_os:
            return hostname_os

        if self.__config.key("hostname"):
            return self.__config.key("hostname")

        return self.__default["hostname"]

    def num_workers(self):
        if self.__args.num_workers:
            return self.__args.num_workers

        num_workers_os = os.environ.get("NOTIFIER_NUM_WORKERS")
        if num_workers_os:
            return num_workers_os

        if self.__config.key("num_workers"):
            return self.__config.key("num_workers")

        return self.__default["num_workers"]

    def log_from(self):
        if self.__args.log_from:
            return self.__args.log_from

        log_from_os = os.environ.get("NOTIFIER_LOG_FROM")
        if log_from_os:
            return log_from_os

        if self.__config.key("log_from"):
            return self.__config.key("log_from")

        return self.__default["log_from"]

    def log_path(self):
        if self.__args.log_path:
            return self.__args.log_path

        log_path_os = os.environ.get("NOTIFIER_LOG_PATH")
        if log_path_os:
            return log_path_os

        if self.__config.key("log_path"):
            return self.__config.key("log_path")

        return self.__default["log_path"]

    def pid_path(self):
        if self.__args.pid_path:
            return self.__args.pid_path

        pid_path_os = os.environ.get("NOTIFIER_PID_PATH")
        if pid_path_os:
            return pid_path_os

        if self.__config.key("pid_path"):
            return self.__config.key("pid_path")

        return self.__default["pid_path"]
