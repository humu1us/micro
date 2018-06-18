import os
from celery import Celery


class MicroApp(Celery):
    def __init__(self, broker, queue, hostname, workers, log_path, pid_path):

        self.__namespace = "Micro"
        self.__broker_url = broker
        self.__queue = queue
        self.__hostname = hostname
        self.__workers = workers
        self.__log_path = log_path
        self.__pid_path = pid_path

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
