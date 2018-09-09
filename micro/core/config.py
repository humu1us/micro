import json


class Config:
    def __init__(self, path=None):
        self.__conf = {}
        if path:
            self.__load(path)

    def __load(self, path):
        with open(path) as conf_file:
            conf_data = conf_file.read()
            self.__conf = json.loads(conf_data)

    def key(self, app, name=None):
        if name:
            try:
                return self.__conf[app][name]
            except KeyError:
                return None
        return self.__conf.get(app, {})

    def replace(self, app, name, new_setting):
        if not self.__conf.get(app):
            self.__conf[app] = {}
        self.__conf[app].update(new_setting)

    def remove(self, app, name):
        try:
            del(self.__conf[app][name])
        except KeyError:
            pass
