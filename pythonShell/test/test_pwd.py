import unittest
from collections import deque
from shell import eval
import os
from unittest.mock import patch


class PwdTest(unittest.TestCase):

    def test_eval_pwd_success(self):
        out = deque()
        eval("pwd", out)
        self.assertEqual(out.popleft(), os.getcwd() + "\n")

    @patch("os.getcwd")
    def test_eval_pwd_oserror(self, mock_getcwd):
        mock_getcwd.side_effect = OSError("Mocked error")
        out = deque()
        with self.assertRaises(OSError):
            eval("pwd", out)

    def test_unsafe_pwd(self):
        out = deque()
        eval("_pwd nondirectory", out)
        self.assertEqual(
            out.pop(), "Directory 'nondirectory/nonfile' not found\n"
        )
