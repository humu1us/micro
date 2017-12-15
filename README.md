# Micro
A platform to create microservices available through Celery API.

## Micro API
Micro uses a very simple API to run, list and get information about plugins:

* `list()`: list all available plugins.
* `info(plugin_name)`: show information about a specific plugin.
* `help(plugin_name)`: show the plugin help.
* `run(plugin_name, params)`: execute the given plugin.

To use this API you can use the [Micro-dev](https://github.com/humu1us/micro-dev) package who provide two important libraries, the access to the Celery API and the PluginBase class who allow writing Micro plugins.

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

# This description is required by Micro
plugin = PluginDescription(
  name="Example Plugin",
  author="Jhon Doe",
  short_desc="A very simple example plugin",
  long_desc="This plugin is a very simple example, "
            "for that reason, we don't have a long description"
  help_str="Params: name type string; A name to greet",
  instance=ExamplePlugin
)
```
Each plugin needs to have its own folder inside of the plugins directory (check the section ["Configuring Micro"](https://github.com/humu1us/micro#configuring-micro) for details)

The plugin directory should look like this:

```
my_plugindir/
	example-plugin/
		interface.py
	other-plugin/
		inteface.py
```

## Configuring Micro
### Parameters priority
Micro can be configurated through CLI, environment variables, config file and/or default values (in that order).

### Command line (CLI)
These arguments are the highest priority for Micro. So, these overwrite any other parameters set by any other method. The CLI arguments that can be used are:

```
$ python -m micro -h
usage: __main__.py [-h] [-b BROKER_URL] [-q QUEUE_NAME] [-H HOSTNAME]
                   [-w NUM_WORKERS] [-l LOG_FROM] [-lp LOG_PATH]
                   [-pp PID_PATH] [--default-params]

optional arguments:
  -h, --help            show this help message and exit
  -b BROKER_URL, --broker-url BROKER_URL
                        Set the broker url
  -q QUEUE_NAME, --queue-name QUEUE_NAME
                        Set the Celery queue name
  -H HOSTNAME, --hostname HOSTNAME
                        Set the hostname for the workers
  -w NUM_WORKERS, --num-workers NUM_WORKERS
                        Set the Celery worker number
  -l LOG_FROM, --log-from LOG_FROM
                        Set the logger level
  -lp LOG_PATH, --log-path LOG_PATH
                        Set the log file path
  -pp PID_PATH, --pid-path PID_PATH
                        Set the pid file path
  --default-params      Show default parameters
```

### Environment variables
The next priority in parameters for Micro are environment variables. The list of environment variables used are:

```
MICRO_CONFIG      # config file location: /path/to/config/config.json
MICRO_PLUGIN_PATH # path to plugin folder: /path/to/plugin/folder
MICRO_BROKER_URL  # broker url: ampq://user:pass@host:port//
MICRO_QUEUE_NAME  # queue name used
MICRO_HOSTNAME    # workers hostname
MICRO_NUM_WORKERS # number of workers to create (integer number)
MICRO_LOG_FROM    # minimun log level to write: DEBUG, INFO, WARNING, ERROR, CRITICAL or FATAL
MICRO_LOG_PATH    # path to log folder: /path/to/log/folder
MICRO_PID_PATH    # path to pid folder: /path/to/pid/folder
```

**IMPORTANT:** `MICRO_CONFIG` and `MICRO_PLUGIN_PATH` variables provide the only way to set config file and plugin folder paths.

### Config file
The lowest priority is the use of a JSON config file. The path to this config file must be set using `MICRO_CONFIG` environment variable.

Config file example:

```js
{
    "broker_url": "ampq://user:pass@host:port//",
    "queue_name": "",
    "hostname": "",
    "num_workers": ,
    "log_from": "",
    "log_path": "/path/to/log/folder",
    "pid_path": "/path/to/pid/folder"
}
```

A config file skeleton can be created using the following command:
`$ python -m micro --default-params > config.json`

### Default values
The default values are:

```
$ python -m micro --default-params
{
    "broker_url": "",
    "queue_name": "micro_queue",
    "hostname": "micro",
    "num_workers": 1,
    "log_from": "INFO",
    "log_path": "/var/log",
    "pid_path": "/var/run"
}
```
