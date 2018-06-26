import os
import sys


def set_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
    except PermissionError:
        sys.exit("ERROR: permission denied: {}".format(path))
