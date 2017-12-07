from argparse import ArgumentParser


class CLI(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.__parse_args()

    def __parse_args(self):
        self.add_argument("-p",
                          "--plugin_path",
                          required=False,
                          help="Set the plugin path")
        self.add_argument("-b",
                          "--broker_url",
                          required=False,
                          help="Set the broker url")
        self.add_argument("-q",
                          "--queue_name",
                          required=False,
                          help="Set the Celery queue name")
        self.add_argument("-H",
                          "--hostname",
                          required=False,
                          help="Set the hostname for the workers")
        self.add_argument("-w",
                          "--num_workers",
                          type=int,
                          required=False,
                          help="Set the Celery worker number")
        self.add_argument("-l",
                          "--log_from",
                          required=False,
                          help="Set the logger level")
        self.add_argument("-lp",
                          "--log_path",
                          required=False,
                          help="Set the log file path")
        self.add_argument("-pp",
                          "--pid_path",
                          required=False,
                          help="Set the pid file path")
        self.add_argument("--default_params",
                          default=False,
                          action='store_true',
                          help="Show default parameters")
