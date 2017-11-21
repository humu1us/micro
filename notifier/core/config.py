import json
import os
from .private.singleton import Singleton


@Singleton
class Config:
    NOTIFIER_CONFIG = "NOTIFIER_CONFIG"

    def __init__(self):
        self.__path = os.environ.get(Config.NOTIFIER_CONFIG, "")

        if not self.__path:
            raise RuntimeError(Config.NOTIFIER_CONFIG + " not defined")

        self.__conf = {}

    def key(self, name):
        if not self.__conf:
            self.reload()

        return self.__conf.get(name, None)

    def reload(self):
        with open(self.__path) as conf_file:
            conf_data = conf_file.read()
            self.__conf = json.loads(conf_data)
