import os
import importlib.util as imp
from .pluginbase import PluginBase
from ..core.logger import log


class PluginManager:
    def __init__(self):
        self.__INTERFACE = "interface.py"
        self.__plugin_path = self.__plugin_path()
        self.__plugins = {}
        self.__load()

    def __plugin_path(self):
        plugin_path = os.environ.get("MICRO_PLUGIN_PATH")

        if not plugin_path:
            raise RuntimeError("MICRO_PLUGIN_PATH not set")

        if not os.path.isdir(plugin_path):
            raise RuntimeError("MICRO_PLUGIN_PATH no name a folder")

        return plugin_path

    def instance(self, name):
        pdesc = self.__plugins.get(name)
        if not pdesc:
            return None

        return pdesc.instance()

    def plugins(self):
        result = {}
        names = self.__plugins.keys()
        for n in names:
            result[n] = self.__plugins[n].short_desc

        return result

    def info(self, name):
        plg = self.__plugins.get(name)

        if not plg:
            return None

        return plg.long_desc

    def help(self, name):
        plg = self.__plugins.get(name)

        if not plg:
            return None
        return plg.help_str

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
        spec = imp.spec_from_file_location("loaded_module", iface)
        module = imp.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not issubclass(module.plugin.instance, PluginBase):
            return None

        return module.plugin
