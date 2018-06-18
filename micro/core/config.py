import os
import json


class Config:
    def __init__(self, path=None):
        self.__conf = {}
        if path:
            self.__load(path)

    def key(self, name):
        return self.__conf.get(name)

    def __load(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("ERROR: config file not found in {}".format(path))

        with open(path) as conf_file:
            conf_data = conf_file.read()
            self.__conf = json.loads(conf_data)
