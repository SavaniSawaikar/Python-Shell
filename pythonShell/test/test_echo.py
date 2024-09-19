import unittest
from collections import deque
from shell import eval


class EchoTest(unittest.TestCase):
    def test_simple_echo(self):
        out = deque()
        eval("echo foo", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_echo_no_args(self):
        out = deque()
        eval("echo", out)
        self.assertEqual(out.popleft(), "\n")
        self.assertEqual(len(out), 0)

    def test_echo(self):
        out = deque()
        eval("echo hello world", out)
        self.assertEqual(out.popleft(), "hello world\n")

    def test_echo_exception_type(self):
        out = deque()
        eval("_echo hello world", out)
        self.assertEqual(out.popleft(), "hello world\n")
