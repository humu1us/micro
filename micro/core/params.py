import inspect
import json
import os
import sys
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from .. import __version__
from . import setting
from .config import Config
from .setting import ConfigFile
from .setting import CELERY
from .setting import GUNICORN
from .settingbase import SettingBase

CONF_CELERY = "MICRO_CONFIG_CELERY"
CONF_GUNICORN = "MICRO_CONFIG_GUNICORN"


def add_static_method(cls, name, env, type):
    def get_env():
        return type(os.environ.get("_" + env))

    staticmethod(setattr(cls, name, get_env))


class Params:
    def __init__(self, setall=False):
        self.__get_settings()
        self.__add_methods()
        if setall:
            self.__default = {}
            self.__cli = ArgumentParser(add_help=False,
                                        formatter_class=RawTextHelpFormatter)
            self.__add_args()
            self.__init_settings()
            self.__args = vars(self.__cli.parse_args())
            self.__check_default()
            self.__get_config()

    def __get_settings(self):
        self.__settings = []
        for name, obj in inspect.getmembers(setting):
            if name == ConfigFile.__name__:
                self.__config_setting = obj
                continue

            if inspect.isclass(obj) and obj.__base__ == SettingBase:
                self.__settings.append(obj)

    def __add_methods(self):
        # this method is used to add 'staticmethod'
        # to get the settings from the env vars set
        methods = []
        for s in self.__settings:
            if s.configname:
                continue

            if s.name in methods:
                msg = "There are two settings with the same name: %s" % s.name
                sys.exit(msg)

            methods.append(s.name)
            add_static_method(Params, s.name, s.env, s.type)

    def __add_args(self):
        self.__cli.add_argument("-d",
                                "--default-values",
                                dest="default_values",
                                action="store_true",
                                help="show default values and exit")

        self.__cli.add_argument("-h",
                                "--help",
                                action="help",
                                help="show this help message and exit")

        version = "%(prog)s (version " + __version__ + ")"
        self.__cli.add_argument("-v",
                                "--version",
                                action="version",
                                version=version,
                                help="show program's version and exit")

    def __init_settings(self):
        self.__config_setting = self.__config_setting(self.__cli)

        for i in range(len(self.__settings)):
            self.__settings[i] = self.__settings[i](self.__cli, self.__default)

    def __check_default(self):
        if self.__args.get("default_values"):
            print(json.dumps(self.__default, indent=4))
            sys.exit(0)

    def __get_config(self):
        path = self.__args.get(self.__config_setting.name)
        if not path:
            path = os.environ.get(self.__config_setting.env)

        path = self.__config_setting.validator(path)
        self.__cfg = Config(path)

    def __check_priority(self, setting):
        cli = self.__args.get(setting.name)
        if cli:
            return cli

        if setting.type == bool and setting.env in os.environ:
            return True

        env = os.environ.get(setting.env)
        if env:
            return env

        conf = self.__cfg.key(setting.app, setting.name)
        if conf:
            if isinstance(conf, setting.type):
                return conf
            else:
                msg = "[%s] wrong type from config: %s" % (setting.name, conf)
                sys.exit(msg)

        return setting.default

    def set_params(self):
        for s in self.__settings:
            if not s.env:
                continue

            value = self.__check_priority(s)
            if s.configname:
                self.__cfg.replace(s.app, s.name, {s.configname: value})
                continue

            if s.app and s.app in [CELERY, GUNICORN]:
                self.__cfg.remove(s.app, s.name)

            s.set_value(value)

        os.environ["_" + CONF_CELERY] = json.dumps(self.__cfg.key(CELERY))
        os.environ["_" + CONF_GUNICORN] = json.dumps(self.__cfg.key(GUNICORN))

    @staticmethod
    def namespace():
        return "Micro"

    @staticmethod
    def config_celery():
        return json.loads(os.environ.get("_" + CONF_CELERY))

    @staticmethod
    def config_gunicorn():
        return json.loads(os.environ.get("_" + CONF_GUNICORN))
