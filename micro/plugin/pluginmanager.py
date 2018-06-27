import os
import sys
import json
import importlib.util as imp
from .pluginbase import PluginBase
from ..core.logger import log
from ..core.params import Params


class PluginManager:
    def __init__(self):
        self.__INTERFACE = "interface.py"
        self.__plugin_path = self.__plugin_path()
        self.__plugins = {}
        self.__load()

    def __plugin_path(self):
        path = Params.plugin_path()

        if not os.path.isdir(path):
            sys.exit("ERROR: plugins path no name a folder: {}".format(path))

        return path

    def instance(self, name):
        pdesc = self.__plugins.get(name)
        if not pdesc:
            return None

        return pdesc.instance()

    def plugins(self):
        result = []
        names = self.__plugins.keys()
        for n in names:
            plugin = {
                "name": n,
                "version": self.__plugins[n].version,
                "description": self.__plugins[n].description
            }
            result.append(plugin)

        return json.dumps(result)

    def info(self, name):
        plg = self.__plugins.get(name)

        if not plg:
            return None

        return plg.long_description

    def help(self, name):
        plg = self.__plugins.get(name)

        if not plg:
            return None
        return plg.plugin_help

    def __load(self):
        log.info("Load plugins from: {}".format(self.__plugin_path))
        self.__plugins.clear()
        self.__load_plugins(self.__plugin_path)

    def __load_plugins(self, path):
        for f in os.listdir(path):
            plugin_folder = os.path.join(path, f)
            log.info("Load plugins, checking: {}".format(plugin_folder))
            if not os.path.isdir(plugin_folder):
                msg = "File found in the plugins folder: {}. Omitted" \
                    .format(plugin_folder)
                log.warning(msg)
                continue

            plg = self.__load_plugin_from_file(plugin_folder)
            if not plg:
                msg = "Plugin {} is not valid. Omitted" \
                    .format(plugin_folder)
                log.warning(msg)
                continue

            if not plg.name:
                msg = "Plugin {} does not has name. Omitted" \
                    .format(plugin_folder)
                log.warning(msg)
                continue

            log.info("Plugin found: {}".format(plg.name))
            self.__plugins[plg.name] = plg

    def __load_plugin_from_file(self, path):
        iface = os.path.join(path, self.__INTERFACE)
        if not os.path.exists(iface):
            return None

        sys.path.append(path)
        spec = imp.spec_from_file_location("loaded_module", iface)
        module = imp.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not issubclass(module.plugin.instance, PluginBase):
            return None

        return module.plugin
