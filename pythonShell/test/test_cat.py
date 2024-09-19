import unittest
from collections import deque
from shell import eval
from applications_package import Cat
from tempfile import NamedTemporaryFile
import os
from unittest.mock import patch
import io


class CatTest(unittest.TestCase):
    def test_cat_existing_file(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("Test content\n")
            file_name = tmpfile.name

        eval(f"cat {file_name}", out)
        self.assertEqual(out.popleft(), "Test content\n")

        os.remove(file_name)

    def test_cat_file_not_found(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("cat nonexistentfile.txt", out)

    def test_eval_cat_stdin(self):
        out = deque()
        with patch("sys.stdin", new=io.StringIO("stdin content\n")):
            eval("cat", out)
        self.assertEqual(out.popleft(), "stdin content\n")

    @patch("builtins.open")
    def test_eval_cat_exception_reading_file(self, mock_file):
        mock_file.side_effect = Exception("Mocked error")

        out = deque()
        test_file = "testfile.txt"

        with self.assertRaises(Exception) as context:
            eval(f"cat {test_file}", out)

        self.assertEqual(
            str(context.exception),
            f"Error occurred while reading file '{test_file}': Mocked error",
        )

    def test_unsafe_cat(self):
        out = deque()
        eval("_cat nonfile.txt", out)
        self.assertEqual(out.pop(), "File 'nonfile.txt' not found.\n")

    def test_cat_nonListArgs(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("Test content\n")
            file_name = tmpfile.name

        Cat.exec(file_name, out)
        self.assertEqual(out.popleft(), "Test content\n")
        os.remove(file_name)

    def test_cat_empty_file(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            file_name = tmpfile.name

        eval(f"cat {file_name}", out)
        self.assertEqual(out, [])

    def test_cat_line_without_newline(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("Line without newline")
            file_name = tmpfile.name

        eval(f"cat {file_name}", out)
        self.assertEqual(out, ["Line without newline\n"])
