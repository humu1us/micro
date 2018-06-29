from multiprocessing import Process
from .celeryapp import CeleryApp
from .params import Params


def start_celery():
    celery = CeleryApp()
    celery.start_app()


class MicroApp():
    def __init__(self):
        self.__celery = Params.celery()
        self.__flask = Params.api_rest()

    def __start_celery(self):
        if not self.__celery:
            # TODO: this print must be logged
            print("CeleryApp not started")
            return

        proc = Process(target=start_celery)
        proc.start()

    def __start_flask(self):
        if not self.__flask:
            # TODO: this print must be logged
            print("FlaskApp not started")
            return

        # TODO: implement FlaskAPP class
        pass

    def start(self):
        self.__start_celery()
        self.__start_flask()
