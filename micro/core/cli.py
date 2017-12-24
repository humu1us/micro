from argparse import ArgumentParser
from argparse import REMAINDER
from argparse import SUPPRESS


class CLI(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.__parse_args()

    def __parse_args(self):
        self.add_argument("-b",
                          "--broker-url",
                          required=False,
                          help="Set the broker url")
        self.add_argument("-q",
                          "--queue-name",
                          required=False,
                          help="Set the Celery queue name")
        self.add_argument("-H",
                          "--hostname",
                          required=False,
                          help="Set the hostname for the workers")
        self.add_argument("-w",
                          "--num-workers",
                          type=int,
                          required=False,
                          help="Set the Celery worker number")
        self.add_argument("-lp",
                          "--log-path",
                          required=False,
                          help="Set the log file path")
        self.add_argument("-pp",
                          "--pid-path",
                          required=False,
                          help="Set the pid file path")
        self.add_argument("--default-params",
                          default=False,
                          action="store_true",
                          help="Show default parameters")
        self.add_argument("ignored",
                          nargs=REMAINDER,
                          help=SUPPRESS)
