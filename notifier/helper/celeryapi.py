from ..core.config import Config

NAMESPACE = "Notifier"


def celery_name(function_name):
    return NAMESPACE + "." + function_name


def queue():
    return Config.instance().key("queue_name")


def plugin_path():
    return Config.instance().key("plugin_path")
