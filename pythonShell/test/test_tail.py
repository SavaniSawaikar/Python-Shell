import unittest
from collections import deque
from shell import eval
from applications_package import Tail
import os
from unittest.mock import patch
from tempfile import NamedTemporaryFile


class TailTest(unittest.TestCase):
    def test_tail_len_2(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("tail file.txt 2", out)

    def test_tail_length_three(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("tail 2 3 file.txt", out)

    def test_tail_valid_file(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            for i in range(15):
                tmpfile.write(f"Line {i + 1}\n")
            file_name = tmpfile.name

        # Pass the filename without quotes
        eval(f"tail {file_name}", out)
        self.assertEqual(len(out), 10)
        self.assertEqual(out.popleft(), "Line 6\n")

        os.remove(file_name)

    def test_tail_custom_line_count(self):
        out = deque()
        line_count = 5
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            for i in range(10):
                tmpfile.write(f"Line {i + 1}\n")
            file_name = tmpfile.name

        eval(f"tail -n {line_count} {file_name}", out)
        self.assertEqual(len(out), line_count)

        os.remove(file_name)

    def test_tail_file_not_found(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("tail nonexistentfile.txt", out)

    @patch("builtins.open")
    def test_eval_tail_exception_reading_file(self, mock_file):
        # Setting up the mock to raise an exception
        mock_file.side_effect = Exception("Mocked error")

        out = deque()
        test_file = "testfile.txt"

        # Execute the eval function and check for a general Exception
        with self.assertRaises(Exception) as context:
            eval(f"tail {test_file}", out)

        # Verify the exception message
        self.assertEqual(
            str(context.exception),
            f"Error reading file '{test_file}': Mocked error",
        )

    def test_tail_wrong_number_of_args(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("tail", out)

        with self.assertRaises(ValueError):
            eval("tail -n 10 file1.txt file2.txt", out)

    def test_tail_invalid_line_count(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("tail -n not-a-number somefile.txt", out)

    def test_tail_wrong_flag(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("tail -x 10 somefile.txt", out)

    def test_unsafe_tail(self):
        out = deque()
        eval("_tail nonfile.txt", out)
        self.assertEqual(out.pop(), "File 'nonfile.txt' not found\n")

    def test_tail_nonListArgs(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("line 1\n")
            tmpfile.write("line 2\n")
            tmpfile.write("line 3\n")
            file_name = tmpfile.name
        Tail.exec(file_name, out)
        self.assertEqual(out.pop(), "line 3\n")
        self.assertEqual(out.pop(), "line 2\n")
        self.assertEqual(out.pop(), "line 1\n")
        os.remove(file_name)
