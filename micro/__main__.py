from .core.microapp import MicroApp
from .core.params import Params


def main():
    Params()

    app = MicroApp()
    app.start()


if __name__ == "__main__":
    main()
