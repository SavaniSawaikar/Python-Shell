import unittest
from collections import deque
from shell import eval
from applications_package import Sort
from unittest.mock import patch
import io


class SortTest(unittest.TestCase):
    def test_sort_default(self):
        out = deque()
        input_lines = ["apple\n", "banana\n", "orange\n"]
        Sort.exec([], out, input_stream=input_lines)

    def test_sort_reverse(self):
        out = deque()
        input_lines = ["apple\n", "banana\n", "orange\n"]
        Sort.exec(["-r"], out, input_stream=input_lines)

    def test_sort_with_file(self):
        input_lines = ["apple\n", "banana\n", "orange\n"]
        with patch("builtins.open", new_callable=io.StringIO) as mock_file:
            mock_file.return_value.writelines(input_lines)

    def test_sort_file_not_found(self):
        out = deque()
        with self.assertRaises(IOError):
            Sort.exec(["nonexistent_file.txt"], out)

    def test_sort_invalid_option(self):
        out = deque()
        with self.assertRaises(ValueError):
            Sort.exec(["-x"], out)

    def test_sort_exception_reading_file(self):
        out = deque()
        with patch("builtins.open", side_effect=IOError("Mocked error")):
            with self.assertRaises(IOError):
                Sort.exec(["file.txt"], out)

    def test_unsafe_sort(self):
        out = deque()
        eval("_sort nonfile.txt", out)
        self.assertEqual(
            out.pop(), "sort: nonfile.txt: No such file or directory\n"
        )
