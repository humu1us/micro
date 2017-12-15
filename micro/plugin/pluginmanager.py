import os
import importlib.util as imp
from .pluginbase import PluginBase


class PluginManager:
    def __init__(self):
        self.__INTERFACE = "interface.py"
        self.__plugin_path = self.__plugin_path()
        self.__plugins = {}
        self.__load()

    def __plugin_path(self):
        plugin_path = os.environ.get("NOTIFIER_PLUGIN_PATH")

        if not plugin_path:
            raise RuntimeError("NOTIFIER_PLUGIN_PATH not set")

        if not os.path.isdir(plugin_path):
            raise RuntimeError("NOTIFIER_PLUGIN_PATH no name a folder")

        return plugin_path

    def instance(self, name):
        pdesc = self.__plugins.get(name, None)
        if not pdesc:
            return None

        return pdesc.instance()

    def list(self):
        result = {}
        names = self.__plugins.keys()
        for n in names:
            result[n] = self.__plugins[n].short_desc

        return result

    def info(self, name):
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
        self.__load_plugins(self.__plugin_path)

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
