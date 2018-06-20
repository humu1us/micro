import os
import sys


def set_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
    except PermissionError:
        sys.stderr.write("ERROR: permission denied: {}".format(path))
        sys.exit(1)
