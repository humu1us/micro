class PluginBase:
    def run():
        err = "Error, this is an abstract method " \
              "you need implement this in a derived class"
        raise NotImplementedError(err)


class PluginDescription:
    def __init__(self,
                 name,
                 author,
                 short_desc,
                 long_desc,
                 help_str,
                 instance):
        self.name = name
        self.author = author
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.help_str = help_str
        self.instance = instance
