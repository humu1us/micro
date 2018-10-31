from .core.microapp import MicroApp
from .core.params import Params


def main():
    params = Params(setall=True)
    params.set_params()

    app = MicroApp()
    app.start()


if __name__ == "__main__":
    main()
