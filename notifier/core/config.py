import json
import os


class Config:
    def __init__(self):
        self.__NOTIFIER_CONFIG = "NOTIFIER_CONFIG"
        self.__path = os.environ.get(self.__NOTIFIER_CONFIG, "")

        if not self.__path:
            raise RuntimeError(self.__NOTIFIER_CONFIG + " not defined")

        self.__conf = {}
        self.__load()

    def key(self, name):
        return self.__conf.get(name, None)

    def __load(self):
        with open(self.__path) as conf_file:
            conf_data = conf_file.read()
            self.__conf = json.loads(conf_data)
