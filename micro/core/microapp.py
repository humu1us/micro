from multiprocessing import Process
from .celeryapp import CeleryApp


def start_celery():
    celery = CeleryApp()
    celery.start_app()


class MicroApp():
    def __run_celery(self):
        proc = Process(target=start_celery)
        proc.start()

    def start(self):
        self.__run_celery()
