# Micro
A platform to create microservices available through Celery API.

## Micro API
Micro uses a very simple API to run, list and get information about plugins:

* `plugins()`: list all available plugins.
* `info(plugin_name)`: show information about a specific plugin.
* `help(plugin_name)`: show the plugin help.
* `run(plugin_name, params)`: execute the given plugin.

To use this API you can use the [Micro-dev](https://github.com/humu1us/micro-dev) package who provide two important libraries, the access to the Celery API and the PluginBase class who allow writing Micro plugins.

### API example

```python
>>> from micro.api.endpoints import plugins, run
>>>
>>> plugins.delay().wait()
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


## Installation

PyPi

```
$ pip install micro
```


Development version:

```
$ git clone git@github.com:humu1us/micro.git
$ cd micro
$ pip install .
```

or direct from repo

```
$ pip install git+ssh://git@github.com/humu1us/micro.git
```

## Configuration
### Parameters priority
Micro can be configurated through CLI, environment variables, config file and/or default values (in that order).

### Command line (CLI)
These arguments are the highest priority for Micro. So, these overwrite any other parameters set by any other method. The CLI arguments that can be used are:

```
$ micro -h
usage: micro [-h] [-b BROKER_URL] [-q QUEUE_NAME] [-H HOSTNAME]
             [-w NUM_WORKERS] [-lp LOG_PATH] [-pp PID_PATH]
             [--default-params]

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
  -lp LOG_PATH, --log-path LOG_PATH
                        Set the log file path
  -pp PID_PATH, --pid-path PID_PATH
                        Set the pid file path
  --default-params      Show default parameters
```

### Environment variables
The next priority in parameters for Micro are environment variables. The list of environment variables used are:

```
MICRO_CONFIG             # config file location: /path/to/config/config.json
MICRO_PLUGIN_PATH        # path to plugin folder: /path/to/plugin/folder
MICRO_LOG_PATH           # path to log folder: /path/to/plugin/folder
MICRO_LOG_FROM           # minimun log level to write: DEBUG, INFO, WARNING, ERROR, CRITICAL or FATAL
MICRO_BROKER_URL         # broker url: ampq://user:pass@host:port//
MICRO_QUEUE_NAME         # queue name used
MICRO_HOSTNAME           # workers hostname
MICRO_NUM_WORKERS        # number of workers to create (integer number)
MICRO_CELERY_LOG_PATH    # path to Celery log folder: /path/to/celery/log/folder
MICRO_CELERY_PID_PATH    # path to Celery pid folder: /path/to/celery/pid/folder
```

**IMPORTANT:** `MICRO_CONFIG`, `MICRO_PLUGIN_PATH`, `MICRO_LOG_PATH` and `MICRO_LOG_FROM` variables provide the only way to set config file, the plugin folder path, the logger file path and the logger level.

### Config file
The lowest priority is the use of a JSON config file. The path to this config file must be set using `MICRO_CONFIG` environment variable.

Config file example:

```js
{
    "broker_url": "ampq://user:pass@host:port//",
    "queue_name": "",
    "hostname": "",
    "num_workers": ,
    "log_path": "/path/to/log/folder",
    "pid_path": "/path/to/pid/folder"
}
```

A config file skeleton can be created using the following command:
`$ micro --default-params > config.json`

### Default values
The default values are:

```
$ micro --default-params
{
    "broker_url": "",
    "queue_name": "micro_queue",
    "hostname": "micro",
    "num_workers": 1,
    "log_path": "/var/log",
    "pid_path": "/var/run"
}
```

## Docker

### Pull
To download from Docker Hub

```
$ docker pull humu1us/micro:<version>
```
To check the version please visit [Micro's repository on Docker Hub](https://hub.docker.com/r/humu1us/micro/)

### Build
To build the container first move to the branch/tag to use and then use the following command

```
$ docker build -t micro:0.0.1 .
```

At this moment `0.0.1` is the recommended version.

### Run
Run Micro as container is pretty easy and only needs to define `MICRO_BROKER_URL` to set the amqp host. All Micro environment variables are available with `-e` flag, for example:

```
$ docker run -e MICRO_BROKER_URL="amqp://guest:guest@my_host:5672//" -e MICRO_NUM_WORKERS=5 micro:0.0.1
```

The `MICRO_BROKER_URL` is the only mandatory environment variable to use


## Tests

Run all unit tests with:

```
$ python setup.py test
```
