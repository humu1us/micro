from micro.plugin.pluginbase import PluginBase
from micro.plugin.pluginbase import PluginDescription


class ExamplePluginNoDict(PluginBase):
    # This is the method executed by Micro
    def run(self, name):
        return "Hello " + name + "!!!"


# This description is required by Micro
plugin = PluginDescription(
    instance=ExamplePluginNoDict,
    name="Example Plugin No Dict",
    author="Jhon Doe",
    description="A very simple example plugin",
    long_description="This plugin is a very simple example, "
                     "for that reason, we don't have a long description",
    plugin_help="Params: name type string; A name to greet"
)
