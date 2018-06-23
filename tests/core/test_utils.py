from unittest import TestCase
from micro.core.utils import set_folder


class TestUtils(TestCase):
    def test_set_folder(self):
        fake_path = "/fakemicro-test/path"
        with self.assertRaises(SystemExit) as se:
            set_folder(fake_path)

        err = "ERROR: permission denied: " + fake_path
        self.assertEqual(se.exception.args[0], err)
