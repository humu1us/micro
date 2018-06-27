from argparse import ArgumentParser


class CLI(ArgumentParser):
    def __init__(self):
        super().__init__(add_help=False)
        self.description = "Micro arguments:"
        self.__required_args()
        self.__optional_args()

    def __required_args(self):
        self.req = self.add_argument_group("required arguments")
        self.req.add_argument("-p",
                              "--plugin-path",
                              required=False,
                              help="path to the plugins folder")
        self.req.add_argument("-b",
                              "--broker-url",
                              required=False,
                              help="RabbitMQ URL")
        self.req.add_argument("-q",
                              "--queue-name",
                              required=False,
                              help="RabbitMQ queue name")

    def __optional_args(self):
        self.opt = self.add_argument_group("optional arguments")
        self.opt.add_argument("--celery",
                              default=False,
                              action="store_true",
                              help="plugins available through Celery")
        self.opt.add_argument("--api-rest",
                              default=False,
                              action="store_true",
                              help="plugins available through API Rest")
        self.opt.add_argument("--default-params",
                              default=False,
                              action="store_true",
                              help="show default parameters")
        self.opt.add_argument("--version",
                              default=False,
                              action="store_true",
                              help="show Micro version")
        self.opt.add_argument("-h",
                              "--help",
                              action="help",
                              help="Show this help message")
        self.opt.add_argument("-c",
                              "--config-file",
                              required=False,
                              help="path to the config file")
        self.opt.add_argument("-H",
                              "--hostname",
                              required=False,
                              help="Celery worker's hostname")
        self.opt.add_argument("-w",
                              "--num-workers",
                              type=int,
                              required=False,
                              help="set the Celery worker number")
        msg = "log level: DEBUG, INFO, WARNING, ERROR, CRITICAL or FATAL"
        self.opt.add_argument("-ll",
                              "--log-level",
                              required=False,
                              help=msg)
        self.opt.add_argument("-lp",
                              "--log-path",
                              required=False,
                              help="log file path")
        self.opt.add_argument("-cll",
                              "--celery-log-level",
                              required=False,
                              help="Celery " + msg)
        self.opt.add_argument("-clp",
                              "--celery-log-path",
                              required=False,
                              help="Celery log file path")
        self.opt.add_argument("-cpp",
                              "--celery-pid-path",
                              required=False,
                              help="Celery PIDs path")
