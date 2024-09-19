import unittest
from collections import deque
from custom_errors.customFileNotFoundError import CustomFileNotFoundError
from shell import eval
from applications_package import Grep
from tempfile import NamedTemporaryFile
import os
from unittest.mock import patch


class GrepTest(unittest.TestCase):
    def test_grep_successful_match(self):
        out = deque()
        pattern = "test"
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("test line 1\n")
            tmpfile.write("another line\n")
            file_name = tmpfile.name

        eval(f"grep {pattern} {file_name}", out)
        self.assertEqual(out.popleft(), "test line 1\n")

        os.remove(file_name)

    def test_grep_file_not_found():
        out = []
        non_existent_file = "nonexistentfile.txt"
        try:
            Grep.exec(["pattern", non_existent_file], out)
            assert False, "CustomFileNotFoundError was not raised"
        except CustomFileNotFoundError as e:
            assert (
                str(e) == non_existent_file
            )  # Check if the exception message is correct

    def test_grep_multiple_files(self):
        out = deque()
        pattern = "test"
        with NamedTemporaryFile(
            mode="w+", delete=False
        ) as tmpfile1, NamedTemporaryFile(mode="w+", delete=False) as tmpfile2:
            tmpfile1.write("test line 1\n")
            file_name1 = tmpfile1.name
            tmpfile2.write("test line 2\n")
            file_name2 = tmpfile2.name

        eval(f"grep {pattern} {file_name1} {file_name2}", out)
        self.assertEqual(out.popleft(), f"{file_name1}:test line 1\n")
        self.assertEqual(out.popleft(), f"{file_name2}:test line 2\n")

        os.remove(file_name1)
        os.remove(file_name2)

    def test_grep_multiple_files_one_not_found(self):
        out = deque()
        pattern = "test"
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("test line 1\n")
            file_name = tmpfile.name

        with self.assertRaises(FileNotFoundError):
            eval(f"grep {pattern} {file_name} /nonexistent/file", out)

        # os.remove(file_name)

    def test_grep_invalid_regex(self):
        out = deque()
        pattern = "["
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("test line 1\n")
            file_name = tmpfile.name

        with self.assertRaises(ValueError):
            eval(f"grep {pattern} {file_name}", out)

        # os.remove(file_name)

    def test_invalid_number_of_args(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("grep pattern", out)

    @patch("builtins.open", side_effect=Exception("Mocked error"))
    def test_eval_grep_exception_reading_file(self, mock_open): # noqa F811
        out = deque()
        pattern = "test"
        test_file = "testfile.txt"

        with self.assertRaises(Exception):
            eval(f'grep "{pattern}" {test_file}', out)

    def test_unsafe_grep_argCount(self):
        out = deque()
        eval("_grep nonfile.txt", out)
        self.assertEqual(out.pop(), "Wrong number of command line arguments\n")

    def test_unsafe_grep_fileMissing(self):
        out = deque()
        eval("_grep nonfile.txt anotherfile.txt", out)
        self.assertEqual(out.pop(), "File 'anotherfile.txt' not found\n")
