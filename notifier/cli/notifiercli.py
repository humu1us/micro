import argparse


def args():
    args = argparse.ArgumentParser(epilog=__doc__)

    args.add_argument("-p",
                      "--plugin_path",
                      required=False,
                      help="Set the plugin path")

    args.add_argument("-b",
                      "--broker_url",
                      required=False,
                      help="Set the broker url")

    args.add_argument("-q",
                      "--queue_name",
                      required=False,
                      help="Set the Celery queue name")

    args.add_argument("-H",
                      "--hostname",
                      required=False,
                      help="Set the hostname for the workers")

    args.add_argument("-w",
                      "--num_workers",
                      type=int,
                      required=False,
                      help="Set the Celery worker number")

    args.add_argument("-l",
                      "--log_from",
                      required=False,
                      help="Set the logger level")

    args.add_argument("-lf",
                      "--log_file",
                      required=False,
                      help="Set the log file path")

    args.add_argument("-pf",
                      "--pid_file",
                      required=False,
                      help="Set the pid file path")

    return args.parse_args()
