import sys
from flask import Flask
from flask_cors import CORS
from gunicorn import debug
from gunicorn import util
from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems
from ..api.apirest import endpoints
from .params import Params


class GunicornApp(BaseApplication):
    def __init__(self):
        Params()
        self.__namespace = Params.namespace()
        self.__app = Flask(self.__namespace)
        self.__app.register_blueprint(endpoints)
        self.__options = {
            "daemon": True,
            "loglevel": Params.log_level()
        }
        self.__options.update(Params.config_gunicorn())
        super().__init__()

    def load_config(self):
        for key, value in iteritems(self.__options):
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)
            elif key == "cors" and value is not None:
                CORS(self.__app, **value)

    def load(self):
        return self.__app

    def run(self):
        if self.cfg.check_config:
            try:
                self.load()
            except Exception:
                msg = "Error while loading the application"
                sys.exit(msg)

            sys.exit(0)

        if self.cfg.spew:
            debug.spew()

        if self.cfg.daemon:
            util.daemonize(self.cfg.enable_stdio_inheritance)

        super().run()
