from ..core.celery import NotifierApp

app = NotifierApp.instance()


@app.task(queue="notifier_queue")
def add(x, y):
    return x + y
