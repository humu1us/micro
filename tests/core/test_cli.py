from unittest import TestCase
from micro.core.cli import CLI


class TestCLI(TestCase):
    def setUp(self):
        self.cli = CLI()
        self.args = self.cli.parse_args([
            "-b", "url://user:pass@1234//",
            "-q", "queue name",
            "-H", "example_hostname",
            "-w", "5",
            "-lp", "/path/to/the/logs",
            "-pp", "/path/to/the/pids",
            "--default-params"
        ])

    def test_types(self):
        self.assertEqual(type(self.args.broker_url), str)
        self.assertEqual(type(self.args.queue_name), str)
        self.assertEqual(type(self.args.hostname), str)
        self.assertEqual(type(self.args.num_workers), int)
        self.assertEqual(type(self.args.log_path), str)
        self.assertEqual(type(self.args.pid_path), str)
        self.assertEqual(type(self.args.default_params), bool)

    def test_arguments(self):
        self.assertEqual(self.args.broker_url, "url://user:pass@1234//")
        self.assertEqual(self.args.queue_name, "queue name")
        self.assertEqual(self.args.hostname, "example_hostname")
        self.assertEqual(self.args.num_workers, 5)
        self.assertEqual(self.args.log_path, "/path/to/the/logs")
        self.assertEqual(self.args.pid_path, "/path/to/the/pids")
        self.assertTrue(self.args.default_params)

    def test_defaul_params_arg(self):
        args = self.cli.parse_args(["-w", "3"])
        self.assertFalse(args.default_params)
