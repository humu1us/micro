from unittest import TestCase
from micro.core.utils import set_folder
from tests.utils.fakestdout import StdoutLock


class TestUtils(TestCase):
    def test_set_folder(self):
        fake_path = "/fakemicro-test/path"
        with StdoutLock() as lock:
            with self.assertRaises(SystemExit):
                set_folder(fake_path)

        msg = "ERROR: permission denied: " + fake_path
        self.assertEqual(lock.stderr, msg)
