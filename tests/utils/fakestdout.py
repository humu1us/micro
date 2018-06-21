import io
import sys


class FakeStdout:
    def write(self, msg):
        pass


class StdoutLock:
    def __enter__(self):
        self.real_stdout = sys.stdout
        self.real_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        self.stdout = sys.stdout.getvalue()
        self.stderr = sys.stderr.getvalue()
        sys.stdout = self.real_stdout
        sys.stderr = self.real_stderr
