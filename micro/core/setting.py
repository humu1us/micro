from .settingbase import SettingBase
from .validate import Validate

MICRO = "micro"
CELERY = "celery"
GUNICORN = "gunicorn"


class Celery(SettingBase):
    name = "celery"
    cli = ["-C", "--celery"]
    env = "MICRO_CELERY"
    type = bool
    action = "store_true"
    validator = Validate.bool
    description = "plugins available through Celery"


class Gunicorn(SettingBase):
    name = "gunicorn"
    cli = ["-G", "--gunicorn"]
    env = "MICRO_GUNICORN"
    type = bool
    action = "store_true"
    validator = Validate.bool
    description = "plugins available through API Rest"


class ConfigFile(SettingBase):
    name = "config_file"
    cli = ["-c", "--config-file"]
    env = "MICRO_CONFIG_FILE"
    type = str
    validator = Validate.file_exist
    description = "path to the config file"


class PluginPath(SettingBase):
    app = MICRO
    name = "plugin_path"
    cli = ["-p", "--plugin-path"]
    env = "MICRO_PLUGIN_PATH"
    type = str
    validator = Validate.folder_exist
    description = "path to the plugins folder"


class LogLevel(SettingBase):
    app = MICRO
    name = "log_level"
    cli = ["-ll", "--log-level"]
    env = "MICRO_LOG_LEVEL"
    type = str
    default = "WARNING"
    validator = Validate.log_level
    description = "Micro's log level"


class LogFolderPath(SettingBase):
    app = MICRO
    name = "log_folder_path"
    cli = ["-lp", "--log-folder-path"]
    env = "MICRO_LOG_FOLDER_PATH"
    type = str
    default = "/var/log/micro"
    validator = Validate.folder_exist
    description = "path to the Micro's log folder"


class LogFileName(SettingBase):
    app = MICRO
    name = "log_file_name"
    cli = ["-ln", "--log-file-name"]
    env = "MICRO_LOG_FILE_NAME"
    type = str
    default = "micro.log"
    description = "Micro's log file name"


class PIDFolderPath(SettingBase):
    app = MICRO
    name = "pid_folder_path"
    cli = ["-pp", "--pid-folder-path"]
    env = "MICRO_PID_FOLDER_PATH"
    type = str
    default = "/var/run/micro"
    validator = Validate.folder_exist
    description = "path to the Micro's PID folder"


class BrokerURL(SettingBase):
    app = CELERY
    name = "broker_url"
    cli = ["-B", "--broker-url"]
    env = "MICRO_BROKER_URL"
    type = str
    configname = "broker_url"
    description = "Celery broker URL"


class TaskQueues(SettingBase):
    app = CELERY
    name = "task_queues"
    cli = ["-q", "--task-queues"]
    env = "MICRO_TASK_QUEUES"
    type = str
    description = "Celery task queues"


class HostName(SettingBase):
    app = CELERY
    name = "hostname"
    cli = ["-H", "--hostname"]
    env = "MICRO_HOSTNAME"
    type = str
    default = "micro"
    description = "Celery worker's hostname"


class CeleryWorkers(SettingBase):
    app = CELERY
    name = "workers"
    cli = ["-cw", "--celery-workers"]
    env = "MICRO_CELERY_WORKERS"
    type = int
    default = 1
    validator = Validate.positive_int
    description = "Celery number of workers"


class Bind(SettingBase):
    app = GUNICORN
    name = "bind"
    cli = ["-b", "--bind"]
    env = "MICRO_BIND"
    type = str
    default = "0.0.0.0:8000"
    configname = "bind"
    description = "Gunicorn bind, HOST:PORT"


class GunicornWorkers(SettingBase):
    app = GUNICORN
    name = "workers"
    cli = ["-gw", "--gunicorn-workers"]
    env = "MICRO_GUNICORN_WORKERS"
    type = int
    default = 1
    configname = "workers"
    validator = Validate.positive_int
    description = "Gunicorn number of workers"
