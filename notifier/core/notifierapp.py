import os
from celery import Celery
from .config import Config
from .private.singleton import Singleton


@Singleton
class NotifierApp(Celery):
    def __init__(self):
        self.__config = Config.instance()
        super().__init__(self.__config.key("app_name"))
        self.conf.update(broker_url=self.__config.key("broker_url"),
                         result_backend="rpc://")

    def __load_args(self):
        log_file = os.path.join(self.__config.key("log_file"), "%N.log")
        pid_file = os.path.join(self.__config.key("pid_file"), "%N.pid")

        args = ["celery",
                "-A", "notifier.api.celery.endpoints",
                "-Q", self.__config.key("queue_name"),
                "-l", self.__config.key("log_from"),
                "--logfile=" + log_file,
                "--pidfile=" + pid_file,
                "multi", "start"]
        workers = self.__create_workers()
        return args + workers

    def __create_workers(self):
        workers = []
        hostname = self.__config.key("hostname")
        worker_name = "worker{num}@{hostname}"

        for i in range(self.__config.key("num_workers")):
            workers.append(worker_name.format(num=(i + 1), hostname=hostname))

        return workers

    def start_app(self):
        self.start(self.__load_args())
