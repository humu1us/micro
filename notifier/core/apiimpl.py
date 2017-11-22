from ..plugin.pluginloader import PluginLoader


class ApiImpl:
    def __init__(self):
        self.__plugin_loader = PluginLoader()

    def plugin_list(self):
        return self.__plugin_loader.all_names()

    def plugin_info(self, name):
        return self.__plugin_loader.long_description(name)

    def notify(self):
        return ""
