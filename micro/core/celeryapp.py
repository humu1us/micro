import os
from celery import Celery
from .params import Params
from ..core.utils import set_folder


class CeleryApp(Celery):
    def __init__(self):

        self.__namespace = "Micro"
        self.__tasks = "micro.api.endpoints"
        self.__broker_url = Params.broker_url()
        self.__queue = Params.queue_name()
        self.__hostname = Params.hostname()
        self.__workers = Params.num_workers()
        self.__log_path = Params.celery_log_path()
        self.__pid_path = Params.celery_pid_path()

        super().__init__(self.__namespace,
                         broker=self.__broker_url,
                         backend="rpc://")
        self.conf.update(worker_hijack_root_logger=False)

    def queue(self):
        return self.__queue

    def function_name(self, name):
        return self.__namespace + "." + name

    def __load_args(self):
        log_path = os.path.join(self.__log_path, "%N.log")
        pid_path = os.path.join(self.__pid_path, "%N.pid")
        set_folder(log_path)
        set_folder(pid_path)

        args = ["celery",
                "-A", self.__tasks,
                "-Q", self.__queue,
                "-b", self.__broker_url,
                "--logfile=" + log_path,
                "--pidfile=" + pid_path,
                "multi", "start"]
        workers = self.__create_workers()
        return args + workers

    def __create_workers(self):
        workers = []
        worker_name = "worker{num}@{hostname}"

        for i in range(self.__workers):
            workers.append(worker_name.format(num=(i + 1),
                                              hostname=self.__hostname))

        return workers

    def start_app(self):
        self.start(self.__load_args())
