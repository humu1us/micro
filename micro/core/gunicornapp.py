from flask import Flask
from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems
from ..api.apirest import endpoints
from .params import Params


class GunicornApp(BaseApplication):
    def __init__(self):
        self.__namespace = Params.namespace()
        self.__bind = Params.bind()
        self.__num_workers = Params.num_workers()
        self.__app = Flask(self.__namespace)
        self.__app.register_blueprint(endpoints)
        self.__options = {
            "bind": self.__bind,
            "workers": self.__num_workers,
            "daemon": True,
        }
        super().__init__()

    def load_config(self):
        for key, value in iteritems(self.__options):
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.__app
