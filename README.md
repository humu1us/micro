# Micro
A platform to create microservices availables through Celery API.

## Micro API
Micro use a very simple API to run, list and get information about plugins:

* `list()`: list all availables plugins.
* `info(plugin_name)`: show information about an specific plugin.
* `help(plugin_name)`: show the plugin help.
* `run(plugin_name, params)`: execute the given plugin.

To use this API you can use the [Micro-dev](https://github.com/humu1us/micro-dev) package who provide two important libraries, the access to the Celery API and the PluginBase class who allow to write Micro plugins.

### API example

```python
>>> from micro.api.endpoints import list, run
>>>
>>> list.delay().wait()
{'Example plugin': 'A very simple example plugin'}
>>>
>>> run.delay("Example plugin", name="Micro").wait()
'Hello Micro!!!'
```


## Micro plugins

Write a plugin to Micro is very simple all that you need is create a file named `interface.py` this file defines the plugin as follow:

```python
from micro.plugin.pluginbase import PluginBase
from micro.plugin.pluginbase import PluginDescription


class ExamplePlugin(PluginBase):
   def __init__(self):
       print("This is an example plugin")

# This is the method executed by Micro
   def run(self, **kwargs):
       return "Hello " + kwargs["name"] + "!!!"

# This description is requiered by Micro
plugin = PluginDescription(
   name="Example Plugin",
   author="Jhon Doe",
   short_desc="A very simple example plugin",
   long_desc="This plugin is a very simple example, "
             "for that reason we don't have a long description"
   help_str="Params: name type string; A name to greet",
   instance=ExamplePlugin
)
```
