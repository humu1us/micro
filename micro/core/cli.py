from argparse import ArgumentParser


class CLI(ArgumentParser):
    def __init__(self):
        super().__init__(add_help=False)
        self.description = "Micro arguments:"
        self.__required_args()
        self.__optional_args()

    def __required_args(self):
        self.req = self.add_argument_group("required arguments")
        self.req.add_argument("-c",
                              "--config-file",
                              required=False,
                              help="path to the config file")
        self.req.add_argument("-p",
                              "--plugins-path",
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
        self.opt.add_argument("-H",
                              "--hostname",
                              required=False,
                              help="Celery worker's hostname")
        self.opt.add_argument("-w",
                              "--num-workers",
                              type=int,
                              required=False,
                              help="set the Celery worker number")
        self.opt.add_argument("-lp",
                              "--celery-log-path",
                              required=False,
                              help="Celery log file path")
        self.opt.add_argument("-pp",
                              "--celery-pid-path",
                              required=False,
                              help="Celery PIDs path")
        self.opt.add_argument("--default-params",
                              default=False,
                              action="store_true",
                              help="show default parameters")
        self.opt.add_argument("-h",
                              "--help",
                              action="help",
                              help="Show this help message")
