from micro.plugin.pluginbase import PluginBase
from micro.plugin.pluginbase import PluginDescription


class ExamplePlugin(PluginBase):
    def __init__(self):
        print("This is an example plugin")

    # This is the method executed by Micro
    def run(self, **kwargs):
        return "Hello " + kwargs["name"] + "!!!"


# This description is required by Micro
plugin = PluginDescription(
    name="Example Plugin",
    author="Jhon Doe",
    short_desc="A very simple example plugin",
    long_desc="This plugin is a very simple example, "
              "for that reason, we don't have a long description",
    help_str="Params: name type string; A name to greet",
    instance=ExamplePlugin
)
