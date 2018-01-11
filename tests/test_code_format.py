import os
import pycodestyle
from unittest import TestCase


class TestCodeFormat(TestCase):
    def test_pep8_code(self):
        style = pycodestyle.StyleGuide()
        style.options.max_line_length = 80
        filenames = []
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir))
        path = os.path.join(parent, "micro")
        for root, _, files in os.walk(path):
            python_files = [f for f in files if f.endswith('.py')]
            for pyfile in python_files:
                filename = "{0}/{1}".format(root, pyfile)
                filenames.append(filename)
        check = style.check_files(filenames)
        self.assertEqual(check.total_errors,
                         0,
                         "PEP8 style errors: %d" % check.total_errors)

    def test_pep8_tests(self):
        style = pycodestyle.StyleGuide()
        style.options.max_line_length = 80
        filenames = []
        path = os.path.abspath(os.path.dirname(__file__))
        for root, _, files in os.walk(path):
            python_files = [f for f in files if f.endswith('.py')]
            for pyfile in python_files:
                filename = "{0}/{1}".format(root, pyfile)
                filenames.append(filename)
        check = style.check_files(filenames)
        self.assertEqual(check.total_errors,
                         0,
                         "PEP8 style errors: %d" % check.total_errors)
