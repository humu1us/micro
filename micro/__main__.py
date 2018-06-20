from .core.params import Params
from .core.microapp import MicroApp


def main():
    Params()

    app = MicroApp()
    app.start_app()


if __name__ == "__main__":
    main()
