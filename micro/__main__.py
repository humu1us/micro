from .core.celeryapp import CeleryApp
from .core.params import Params


def main():
    Params()

    app = CeleryApp()
    app.start_app()


if __name__ == "__main__":
    main()
