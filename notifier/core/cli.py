from argparse import ArgumentParser


class CLI(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.__parse_args()

    def __parse_args(self):
        self.add_argument("-p",
                          "--plugin-path",
                          required=False,
                          dest="plugin_path",
                          help="Set the plugin path")
        self.add_argument("-b",
                          "--broker-url",
                          required=False,
                          dest="broker_url",
                          help="Set the broker url")
        self.add_argument("-q",
                          "--queue-name",
                          required=False,
                          dest="queue_name",
                          help="Set the Celery queue name")
        self.add_argument("-H",
                          "--hostname",
                          required=False,
                          help="Set the hostname for the workers")
        self.add_argument("-w",
                          "--num-workers",
                          type=int,
                          required=False,
                          dest="num_workers",
                          help="Set the Celery worker number")
        self.add_argument("-l",
                          "--log-from",
                          required=False,
                          dest="log_from",
                          help="Set the logger level")
        self.add_argument("-lp",
                          "--log-path",
                          required=False,
                          dest="log_path",
                          help="Set the log file path")
        self.add_argument("-pp",
                          "--pid-path",
                          required=False,
                          dest="pid_path",
                          help="Set the pid file path")
        self.add_argument("--default-params",
                          default=False,
                          action="store_true",
                          dest="default_params",
                          help="Show default parameters")
