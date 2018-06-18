from .core.params import Params
from .core.microapp import MicroApp


def main():
    params = Params()

    broker = params.broker_url()
    queue = params.queue_name()
    hostname = params.hostname()
    workers = params.num_workers()
    log_path = params.celery_log_path()
    pid_path = params.celery_pid_path()

    app = MicroApp(broker, queue, hostname, workers, log_path, pid_path)
    app.start_app()


if __name__ == "__main__":
    main()
