import unittest
from collections import deque
from shell import eval
from applications_package import Head
import os
from unittest.mock import patch
from tempfile import NamedTemporaryFile


class HeadTest(unittest.TestCase):
    def test_head_valid_file(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            for i in range(15):
                tmpfile.write(f"Line {i + 1}\n")
            file_name = tmpfile.name

        # Pass the filename without quotes
        eval(f"head {file_name}", out)
        self.assertEqual(len(out), 10)
        self.assertEqual(out.popleft(), "Line 1\n")

        os.remove(file_name)

    @patch("builtins.open")
    def test_eval_head_exception_reading_file(self, mock_file):
        # Setting up the mock to raise an exception
        mock_file.side_effect = Exception("Mocked error")

        out = deque()
        test_file = "testfile.txt"

        # Execute the eval function and check for a general Exception
        with self.assertRaises(Exception) as context:
            eval(f"head {test_file}", out)

        # Verify the exception message
        self.assertEqual(
            str(context.exception),
            f"Error reading file '{test_file}': Mocked error",
        )

    def test_head_invalid_line_count(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("head -n not-a-number somefile.txt", out)

    def test_head_wrong_flag(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval(
                "head -x 10 somefile.txt", out
            )  # Using an incorrect flag '-x' instead of '-n'

    def test_head_len_2(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("head file.txt 2", out)

    def test_head(self):
        out = deque()
        eval("head file.txt", out)

    def test_head_file_not_found(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("head file.txt", out)

    def test_head_length_three(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("head 2 3 file.txt", out)

    def test_unsafe_head_fileMissing(self):
        out = deque()
        eval("_head nonfile.txt", out)
        self.assertEqual(out.pop(), "File 'nonfile.txt' not found\n")

    def test_head_nonListArgs(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            for i in range(15):
                tmpfile.write(f"Line {i + 1}\n")
            file_name = tmpfile.name

        args = f"{file_name}"
        Head.exec(args, out)
        self.assertEqual(len(out), 10)
        self.assertEqual(out.popleft(), "Line 1\n")
        os.remove(file_name)
