import os
import json
from .logger import log


class Config:
    def __init__(self, path):
        self.__conf = {}
        self.__load(path)

    def key(self, name):
        return self.__conf.get(name)

    def __load(self, path):
        if os.path.exists(path):
            with open(path) as conf_file:
                conf_data = conf_file.read()
                self.__conf = json.loads(conf_data)
        else:
            log.error("Config file not found in {}".format(path))
