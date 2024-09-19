import unittest
from collections import deque
from shell import eval
from applications_package import Find

from unittest.mock import patch, Mock
from pathlib import Path


class FindTest(unittest.TestCase):
    def test_unsafe_find(self):
        out = deque()
        eval("_find -name nonSpecified.txt", out)
        self.assertEqual(out.pop(), "Directory 'nonSpecified.txt' not found\n")

    @patch("src.applications_package.find.Path")
    def test_file_matching(self, mock_path):
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True

        mock_path.return_value.glob.return_value = [
            Path("file1.txt"),
            Path("file2.txt"),
            Path("file3.doc"),
        ]
        pattern = "*.txt"
        args = [pattern, "/fake/directory"]
        out = []
        Find.exec(args, out)

    @patch("src.applications_package.find.Path")
    def test_wrong_number_of_arguments(self, mock_path):
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True

        with self.assertRaises(ValueError) as context:
            Find.exec([], [])

        expected_error_message = "Wrong number of command line arguments"
        self.assertEqual(str(context.exception), expected_error_message)

    def test_eval_find(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("find", out)

    def test_eval_find_default_path(self):
        out = deque()
        eval("find *.txt", out)

    def test_eval_find_invalid_pattern(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("find [invalid_pattern", out)

    def test_eval_find_nonexistent_directory(self):
        # Arrangeƒ
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("find *.txt nonexistent_directory", out)

    def test_find_exec_with_invalid_arguments(self):
        args = []
        out = Mock()

        with self.assertRaises(ValueError):
            Find.exec(args, out)

    def test_find_exec_with_missing_pattern(self):
        args = ["path", "-name", "try"]
        out = Mock()

        with self.assertRaises(ValueError) as context:
            Find.exec(args, out)

        self.assertEqual(
            str(context.exception), "Pattern not specified after -name"
        )
        out.append.assert_not_called()

    def test_find_exec_with_invalid_directory(self):
        args = ["nonexistent_directory", "-name", "pattern"]
        out = Mock()

        with self.assertRaises(FileNotFoundError) as context:
            Find.exec(args, out)

        self.assertEqual(
            str(context.exception),
            "Directory 'nonexistent_directory' not found",
        )
        out.append.assert_not_called()

    def test_find_exec_with_invalid_regex(self):
        args = ["path", "-name", "*invalid_regex"]
        out = Mock()

        with self.assertRaises(ValueError):
            Find.exec(args, out)

    def test_find_exec_with_missing_pattern_after_name(self):
        args = ["path", "-name"]
        out = Mock()

        with self.assertRaises(ValueError):
            Find.exec(args, out)


class FindMockedErrorTest(unittest.TestCase):
    @patch("applications.Find.exec")
    def test_find_exec_with_exception_handling(self, mock_exec):
        args = ["path", "-name", "pattern"]
        out = Mock()
        mock_exec.side_effect = Exception("Simulated error")

        Find._Find.exec(args, out)
