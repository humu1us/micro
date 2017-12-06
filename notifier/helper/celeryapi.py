from ..core.config import Config

NAMESPACE = "Notifier"


def celery_name(function_name):
    return NAMESPACE + "." + function_name
