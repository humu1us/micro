import json
import os


class Config:
    def __init__(self):
        self.__MICRO_CONFIG = "MICRO_CONFIG"
        self.__path = os.environ.get(self.__MICRO_CONFIG, "")
        self.__conf = {}
        if self.__path:
            self.__load()

    def key(self, name):
        return self.__conf.get(name)

    def __load(self):
        with open(self.__path) as conf_file:
            conf_data = conf_file.read()
            self.__conf = json.loads(conf_data)
