import json
import os
from .private.singleton import Singleton


@Singleton
class Config:
    def __init__(self):
        self.__NOTIFIER_CONFIG = "NOTIFIER_CONFIG"
        self.__path = os.environ.get(self.__NOTIFIER_CONFIG, "")

        if not self.__path:
            raise RuntimeError(self.__NOTIFIER_CONFIG + " not defined")

        self.__conf = {}

    def key(self, name):
        if not self.__conf:
            self.reload()

        return self.__conf.get(name, None)

    def reload(self):
        with open(self.__path) as conf_file:
            conf_data = conf_file.read()
            self.__conf = json.loads(conf_data)
