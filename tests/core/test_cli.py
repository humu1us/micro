import unittest
from micro.core.cli import CLI

cli = CLI()
args = cli.parse_args([
    "-b", "url://user:pass@1234//",
    "-q", "queue name",
    "-H", "example_hostname",
    "-w", "5",
    "-l", "WARNING",
    "-lp", "/path/to/the/logs",
    "-pp", "/path/to/the/pids",
    "--default-params"
])


class TestCLI(unittest.TestCase):
    def test_types(self):
        self.assertEqual(type(args.broker_url), str)
        self.assertEqual(type(args.queue_name), str)
        self.assertEqual(type(args.hostname), str)
        self.assertEqual(type(args.num_workers), int)
        self.assertEqual(type(args.log_from), str)
        self.assertEqual(type(args.log_path), str)
        self.assertEqual(type(args.pid_path), str)
        self.assertEqual(type(args.default_params), bool)

    def test_arguments(self):
        self.assertEqual(args.broker_url, "url://user:pass@1234//")
        self.assertEqual(args.queue_name, "queue name")
        self.assertEqual(args.hostname, "example_hostname")
        self.assertEqual(args.num_workers, 5)
        self.assertEqual(args.log_from, "WARNING")
        self.assertEqual(args.log_path, "/path/to/the/logs")
        self.assertEqual(args.pid_path, "/path/to/the/pids")
        self.assertEqual(args.default_params, True)

    def test_defaul_params_arg(self):
        args = cli.parse_args(["-w", "3"])
        self.assertEqual(args.default_params, False)
