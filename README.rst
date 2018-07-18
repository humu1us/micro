Micro
=====

|travis| |coverage| |pypi| |pyversion|

A platform to create microservices available through ``celery`` and
Rest (using ``gunicorn``) APIs.

Micro API
---------

Micro uses a very simple API to run, list and get information about
plugins:

-  ``plugins()``: list all available plugins.
-  ``info(plugin_name)``: show information about a specific plugin.
-  ``help(plugin_name)``: show the plugin help.
-  ``run(plugin_name, params)``: execute the given plugin.

To use this API with Celery you can use the
`Micro-dev <https://github.com/humu1us/micro-dev>`__ package who provides
two important libraries, the access to the Celery API and the PluginBase
class who allow writing Micro plugins. To use it as API Rest you can use
the ``requests`` python library.

API Celery example (using micro-dev)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from micro.api.endpoints import Requests
    >>>
    >>> req = Requests(BROKER_URL, QUEUE_NAME)
    >>>
    >>> req.plugins.delay().wait()
    '[{"name": "Example Plugin", "version": null, "description": "A very simple example plugin"}]'
    >>>
    >>> req.run.delay("Example plugin", name="Micro").wait()
    'Hello Micro!!!'

API Rest example (using requests)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> import requests
    >>>
    >>> url = "http://localhost:8000/plugins"
    >>> response = requests.request("GET", url)
    >>> print(response.text)
    [{"name": "Example Plugin", "version": null, "description": "A very simple example plugin"}]
    >>>
    >>> url = "http://localhost:8000/run/Example%20Plugin"
    >>> payload = '{"name": "Micro"}'
    >>> headers = {'content-type': 'application/json'}
    >>> response = requests.request("POST", url, data=payload, headers=headers)
    >>> print(response.text)
    Hello Micro!!!

Micro plugins
-------------

Write Micro plugins is very simple all that you need is to create
a file called ``interface.py`` this file defines the plugin as follow:

.. code:: python

    from micro.plugin.pluginbase import PluginBase
    from micro.plugin.pluginbase import PluginDescription


    class ExamplePlugin(PluginBase):
        def __init__(self):
            print("This is an example plugin")

        # This is the method executed by Micro
        def run(self, name):
            return "Hello " + name + "!!!"


    # This description is required by Micro
    plugin = PluginDescription(
        instance=ExamplePlugin,
        name="Example Plugin",
        version="0.1.0",
        url="https://github.com/humu1us/micro",
        author="Jhon Doe",
        author_email="jhon.doe@email.com",
        description="A very simple example plugin",
        long_description="This plugin is a very simple example, "
                         "for that reason, we don't have a long description",
        plugin_help="Params: name type string; A name to greet"
    )

Each plugin needs to have its own folder inside of the plugins directory
(check the section `“Configuring
Micro” <https://github.com/humu1us/micro#configuring-micro>`__ for
details)

The plugin directory should look like this:

::

    my_plugindir/
        example-plugin/
            interface.py
            exmple_plugin_core/
                libs...
        other-plugin/
            inteface.py
            other_plugin_core/
                libs...


**IMPORTANT:** All the plugins must provide its own libraries inside of its own
namespace in order to avoid overwritting files. The general recomendation is to
use a base directory with the same name of the plugin as the example above shows

Installation
------------

PyPi:

::

    $ pip install micro

Development version:

::

    $ git clone git@github.com:humu1us/micro.git
    $ cd micro
    $ pip install -e .

or direct from repository:

::

    $ pip install git+ssh://git@github.com/humu1us/micro.git

Configuration
-------------

Parameters priority
~~~~~~~~~~~~~~~~~~~

Micro can be configurated through CLI, environment variables, config
file and/or default values (in that order).

Command line (CLI)
~~~~~~~~~~~~~~~~~~

These arguments are the highest priority for Micro, so these overwrite
any other parameters set by any other method. The CLI arguments that can
be used are:

::

    $ micro -h
    usage: micro [--celery] [--gunicorn] [-p PLUGIN_PATH] [-c CONFIG_FILE]
                 [-b BROKER_URL] [-q QUEUE_NAME] [-H HOSTNAME]
                 [-w NUM_WORKERS] [-bi BIND] [-ll LOG_LEVEL] [-lp LOG_PATH]
                 [-cll CELERY_LOG_LEVEL] [-clp CELERY_LOG_PATH]
                 [-cpp CELERY_PID_PATH] [--default-params] [--version] [-h]

    Micro arguments:

    start services (choose at least one):
      --celery              plugins available through Celery
      --gunicorn            plugins available through API Rest

    required arguments:
      -p PLUGIN_PATH, --plugin-path PLUGIN_PATH
                            path to the plugins folder

    optional arguments:
      -c CONFIG_FILE, --config-file CONFIG_FILE
                            path to the config file
      -b BROKER_URL, --broker-url BROKER_URL
                            RabbitMQ URL
      -q QUEUE_NAME, --queue-name QUEUE_NAME
                            RabbitMQ queue name
      -H HOSTNAME, --hostname HOSTNAME
                            Celery worker's hostname
      -w NUM_WORKERS, --num-workers NUM_WORKERS
                            set the Celery worker number
      -bi BIND, --bind BIND
                            Set the Gunicorn socket bind, HOST:PORT
      -ll LOG_LEVEL, --log-level LOG_LEVEL
                            log level: DEBUG, INFO, WARNING, ERROR, CRITICAL or
                            FATAL
      -lp LOG_PATH, --log-path LOG_PATH
                            log file path
      -cll CELERY_LOG_LEVEL, --celery-log-level CELERY_LOG_LEVEL
                            Celery log level: DEBUG, INFO, WARNING, ERROR,
                            CRITICAL or FATAL
      -clp CELERY_LOG_PATH, --celery-log-path CELERY_LOG_PATH
                            Celery log file path
      -cpp CELERY_PID_PATH, --celery-pid-path CELERY_PID_PATH
                            Celery PIDs path
      --default-params      show default parameters
      --version             show Micro version
      -h, --help            Show this help message

Environment variables
~~~~~~~~~~~~~~~~~~~~~

The next priority in parameters for Micro are environment variables. The
list of environment variables used are:

::

    MICRO_CELERY             # plugins available through Celery
    MICRO_GUNICORN           # plugins available through API Rest (Gunicorn)
    MICRO_PLUGIN_PATH        # path to plugin folder: /path/to/plugin/folder
    MICRO_CONFIG             # config file location: /path/to/config/config.json
    MICRO_BROKER_URL         # broker url: ampq://user:pass@host:port//
    MICRO_QUEUE_NAME         # queue name used
    MICRO_HOSTNAME           # workers hostname
    MICRO_NUM_WORKERS        # number of workers to create (integer number)
    MICRO_GUNICORN_BIND      # Gunicorn socket bind (host:port)
    MICRO_LOG_LEVEL          # minimun log level to write: DEBUG, INFO, WARNING, ERROR, CRITICAL or FATAL
    MICRO_LOG_PATH           # path to log folder: /path/to/plugin/folder
    MICRO_CELERY_LOG_LEVEL   # minimun log level to write: DEBUG, INFO, WARNING, ERROR, CRITICAL or FATAL
    MICRO_CELERY_LOG_PATH    # path to Celery log folder: /path/to/celery/log/folder
    MICRO_CELERY_PID_PATH    # path to Celery pid folder: /path/to/celery/pid/folder

Config file
~~~~~~~~~~~

The lowest priority is the use of a JSON config file. The path to this
config file must be set using ``-c, --config-file`` CLI arguments or
``MICRO_CONFIG`` environment variable.

Config file example:

.. code:: js

    {
        "plugin_path": "/path/to/plugins/folder",
        "broker_url": "ampq://user:pass@host:port//",
        "queue_name": "micro_queue",
        "hostname": "",
        "num_workers": 2,
        "bind": "0.0.0.0:5000",
        "log_level": "WARNING",
    }

A config file skeleton can be created using the following command:
``$ micro --default-params > config.json``

Default values
~~~~~~~~~~~~~~

The default values are:

::

    $ micro --default-params
    {
        "plugin_path": "",
        "broker_url": "",
        "queue_name": "",
        "hostname": "micro",
        "num_workers": 1,
        "bind": "0.0.0.0:8000",
        "log_level": "INFO",
        "log_path": "/var/log/micro",
        "celery_log_level": "INFO",
        "celery_log_path": "/var/log/micro/celery",
        "celery_pid_path": "/var/run/micro/celery"
    }

Docker
------

Pull
~~~~

To download from Docker Hub:

::

    $ docker pull humu1us/micro:<tag>

To check the available tags please visit `Micro’s repository on Docker
Hub <https://hub.docker.com/r/humu1us/micro/>`__

Build
~~~~~

To build the container first move to the branch/tag to use and then use
the following command:

::

    $ docker build -t micro:<tag> .

Run
~~~

All Micro environment variables are available with ``-e`` flag. For
example to run Micro with Celery you can do:

::

    $ docker run -d \
        -v /path/to/plugins:/etc/micro/plugins \
        -v /path/to/log:/var/log/micro \
        -e MICRO_BROKER_URL=amqp://guest:guest@my_host:5672// \
        -e MICRO_QUEUE_NAME=test \
        -e MICRO_HOSTNAME=my_host \
        -e MICRO_NUM_WORKERS=2 \
        -e MICRO_CELERY=1 \
        micro:<tag>

``MICRO_BROKER_URL`` and ``MICRO_QUEUE_NAME`` are the only mandatory
environment variables to set when Celery will be used.

When Micro will be run with API Rest you have to bind the Gunicorn port:

::

    $ docker run -d \
        -v /path/to/plugins:/etc/micro/plugins \
        -v /path/to/log:/var/log/micro \
        -e MICRO_BIND=0.0.0.0:5000 \
        -e MICRO_NUM_WORKERS=2 \
        -e MICRO_GUNICORN=1 \
        -p 5000:5000 \
        micro:<tag>

Tests
-----

Run all unit tests with:

::

    $ python setup.py test

.. |travis| image:: https://img.shields.io/travis/humu1us/micro.svg?style=flat-square
   :target: https://travis-ci.org/humu1us/micro
.. |coverage| image:: https://img.shields.io/coveralls/humu1us/micro.svg?style=flat-square
   :target: https://coveralls.io/github/humu1us/micro
.. |pypi| image:: https://img.shields.io/pypi/v/Micro.svg?style=flat-square
   :target: https://pypi.python.org/pypi/Micro/
.. |pyversion| image:: https://img.shields.io/pypi/pyversions/micro.svg?style=flat-square
   :target: https://pypi.python.org/pypi/Micro/
