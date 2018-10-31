import os


class SettingBase:
    app = None
    cli = None
    env = None
    name = None
    type = None
    action = None
    default = None
    validator = None
    configname = None
    description = None

    def __init__(self, parse=None, defaults=None):
        if parse:
            self.__add_arg(parse)

        if defaults is not None:
            self.__make_defaults(defaults)

    def __add_arg(self, parse):
        if not self.cli:
            return

        args = tuple(self.cli)

        help_msg = "%s\nenv: %s\ndefault: %s" % (self.description,
                                                 self.env,
                                                 self.default)
        kwargs = {
            "dest": self.name,
            "action": self.action or "store",
            "type": self.type or str,
            "default": None,
            "help": help_msg
        }

        if kwargs["action"] != "store":
            kwargs.pop("type")

        parse.add_argument(*args, **kwargs)

    def __make_defaults(self, defaults):
        if not self.app:
            return

        if self.app not in defaults:
            defaults[self.app] = {}

        defaults[self.app][self.name] = self.default or ""

    def set_value(self, value):
        if callable(self.validator):
            value = self.validator(value)

        if value:
            os.environ["_" + self.env] = str(value)
