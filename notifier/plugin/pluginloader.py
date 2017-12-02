import os
import importlib.util as imp
from .pluginbase import PluginBase
from ..core.config import Config


class PluginLoader:
    def __init__(self):
        self.__INTERFACE = "interface.py"
        self.__plugins = {}
        self.__load()

    def instance(self, name):
        pdesc = self.__plugins.get(name, None)
        if not pdesc:
            return None

        return pdesc.instance()

    def list_all(self):
        result = {}
        names = self.__plugins.keys()
        for n in names:
            result[n] = self.__plugins[n].short_desc

        return result

    def long_description(self, name):
        plg = self.__plugins.get(name, None)

        if not plg:
            return None

        return plg.long_desc

    def help(self, name):
        plg = self.__plugins.get(name, None)

        if not plg:
            return None
        return plg.help_str

    def __load(self):
        self.__plugins.clear()
        c = Config.instance()
        self.__load_plugins(c.key("plugin_path"))

    def __load_plugins(self, path):
        if not path:
            return

        for f in os.listdir(path):
            plugin_folder = os.path.join(path, f)
            if not os.path.isdir(plugin_folder):
                continue

            plg = self.__load_plugin_from_file(plugin_folder)
            if not plg:
                continue

            if not plg.name:
                print("Error, no name set, cannot be loaded")
                continue

            self.__plugins[plg.name] = plg

    def __load_plugin_from_file(self, path):
        iface = os.path.join(path, self.__INTERFACE)
        spec = imp.spec_from_file_location("loaded_module", iface)
        module = imp.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not issubclass(module.plugin.instance, PluginBase):
            return None

        return module.plugin
