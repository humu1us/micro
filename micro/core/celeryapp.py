import os
from celery import Celery
from .params import Params
from ..core.utils import set_folder


class CeleryApp(Celery):
    def __init__(self):

        Params()
        self.__tasks = "micro.api.celery"
        self.__namespace = Params.namespace()
        self.__queue = Params.task_queues()
        self.__hostname = Params.hostname()
        self.__workers = Params.workers()
        self.__log_path = os.path.join(Params.log_folder_path(), "celery")
        self.__pid_path = os.path.join(Params.pid_folder_path(), "celery")
        self.__options = {
            "worker_hijack_root_logger": False
        }
        self.__options.update(Params.config_celery())

        super().__init__(self.__namespace)
        self.config_from_object(self.__options)

    def __load_args(self):
        log_path = os.path.join(self.__log_path, "%N.log")
        pid_path = os.path.join(self.__pid_path, "%N.pid")
        set_folder(log_path)
        set_folder(pid_path)

        args = ["celery",
                "-A", self.__tasks,
                "-Q", self.__queue,
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

    def queue(self):
        return self.__queue

    def function_name(self, name):
        return self.__namespace + "." + name

    def start_app(self):
        args = self.__load_args()
        print(args)
        self.start(self.__load_args())
