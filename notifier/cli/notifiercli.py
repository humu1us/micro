import argparse

def args():
    args = argparse.ArgumentParser(epilog=__doc__)

    help_app = "Choose between Celery, Flask or both. Default is both"
    args.add_argument("app",
                      default="all",
                      const="all",
                      nargs="?",
                      choices=["celery", "flask", "all"],
                      help=help_app)

    return args.parse_args()
