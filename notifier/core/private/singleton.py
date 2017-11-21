class Singleton(object):
    def __init__(self, decorated):
        self.__decorated = decorated

    def instance(self):
        try:
            return self.__instance
        except AttributeError:
            self.__instance = self.__decorated()
            return self.__instance

    def __call__(self):
        err = "Singletons must be accessed through 'Instance()' method."
        raise NotImplementedError(err)

    def __instancecheck__(self, inst):
        return isinstance(inst, self.__decorated)
