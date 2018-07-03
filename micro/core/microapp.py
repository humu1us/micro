from multiprocessing import Process
from .celeryapp import CeleryApp
from .logger import Logger
from .params import Params


def start_celery():
    celery = CeleryApp()
    celery.start_app()


class MicroApp():
    def __init__(self):
        self.__log = Logger()
        self.__celery = Params.celery()
        self.__gunicorn = Params.gunicorn()

    def __start_celery(self):
        if not self.__celery:
            self.__log.warning("CeleryApp not started")
            return

        proc = Process(target=start_celery)
        proc.start()

    def __start_gunicorn(self):
        if not self.__gunicorn:
            self.__log.warning("GunicornApp not started")
            return

        # TODO: implement FlaskAPP class
        pass

    def start(self):
        self.__start_celery()
        self.__start_gunicorn()
