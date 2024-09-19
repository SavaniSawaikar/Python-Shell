import unittest
from collections import deque
from shell import eval
import os
from tempfile import TemporaryDirectory, NamedTemporaryFile


class LsTest(unittest.TestCase):
    def test_ls_current_directory(self):
        out = deque()
        eval("ls", out)
        expected_files = [
            f + "\n" for f in os.listdir(os.getcwd()) if not f.startswith(".")
        ]
        self.assertEqual(list(out), expected_files)

    def test_ls_invalid_directory(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("ls /nonexistent/directory", out)

    def test_ls_wrong_num_cmdline_args(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("ls one two", out)

    def test_unsafe_ls(self):
        out = deque()
        eval("_ls nondirectory/nonfile", out)
        self.assertEqual(
            out.pop(), "Directory 'nondirectory/nonfile' not found\n"
        )

    def test_ls_specific_directory(self):
        out = deque()
        with TemporaryDirectory() as test_dir:
            eval(f"ls {test_dir}", out)
            expected_files = [
                f + "\n" for f in os.listdir(test_dir) if not f.startswith(".")
            ]
            self.assertEqual(list(out), expected_files)

    def test_ls_not_a_directory(self):
        out = deque()
        with NamedTemporaryFile() as tmpfile:
            test_file = tmpfile.name
            with self.assertRaises(NotADirectoryError):
                eval(f"ls {test_file}", out)
