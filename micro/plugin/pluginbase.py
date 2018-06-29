class PluginBase:
    def run(self, **kwargs):
        err = "Error, this is an abstract method " \
              "you need implement this in a derived class"
        raise NotImplementedError(err)


class PluginDescription:
    def __init__(self,
                 instance,
                 name,
                 version=None,
                 url=None,
                 author=None,
                 author_email=None,
                 description=None,
                 long_description=None,
                 plugin_help=None):
        self.instance = instance
        self.name = name
        self.version = version
        self.url = url
        self.author = author
        self.author_email = author_email
        self.description = description
        self.long_description = long_description
        self.plugin_help = plugin_help
