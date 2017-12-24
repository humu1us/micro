import os
from celery import Celery
from .params import Params


class MicroApp(Celery):
    def __init__(self):
        params = Params()

        self.__namespace = "Micro"
        self.__queue = params.queue_name()
        self.__broker_url = params.broker_url()
        self.__log_from = params.log_from()
        self.__log_path = params.log_path()
        self.__pid_path = params.pid_path()
        self.__hostname = params.hostname()
        self.__workers = params.num_workers()

        super().__init__("Micro",
                         broker=self.__broker_url,
                         backend="rpc://")
        self.conf.update(CELERYD_HIJACK_ROOT_LOGGER=False)

    def queue(self):
        return self.__queue

    def function_name(self, name):
        return self.__namespace + "." + name

    def __load_args(self):
        log_path = os.path.join(self.__log_path, "%N.log")
        pid_path = os.path.join(self.__pid_path, "%N.pid")

        args = ["celery",
                "-A", "micro.api.endpoints",
                "-Q", self.__queue,
                "-b", self.__broker_url,
                "-l", self.__log_from,
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
