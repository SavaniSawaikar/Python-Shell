import unittest
from collections import deque
from shell import eval
from applications_package import Cut
from tempfile import NamedTemporaryFile
from unittest.mock import patch
import io


class CutTest(unittest.TestCase):
    def test_cut_existing_file(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("Test content\n")
            file_name = tmpfile.name

        eval(f"cut {file_name}", out)

    def test_cut_file_not_found(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("cut nonexistentfile.txt", out)

    def test_eval_cut_stdin(self):
        out = deque()
        with patch("sys.stdin", new=io.StringIO("stdin content\n")):
            eval("cut", out)

    @patch("builtins.open")
    def test_eval_cut_exception_reading_file(self, mock_file):
        mock_file.side_effect = Exception("Mocked error")

        out = deque()
        test_file = "testfile.txt"

        with self.assertRaises(Exception) as context:
            eval(f"cut {test_file}", out)

        self.assertEqual(
            str(context.exception),
            f"Error occurred while reading file '{test_file}': Mocked error",
        )

    def test_unsafe_cut(self):
        out = deque()
        eval("_cut nonfile.txt", out)
        self.assertEqual(out.pop(), "File 'nonfile.txt' not found.\n")

    def test_cut_nonListArgs(self):
        out = deque()
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("Test content\n")
            file_name = tmpfile.name

        Cut.exec(file_name, out)

    def test_cut_with_file_input(self):
        file_content = "abcdefg\nhijklmnop\n"
        with open("test_file.txt", "w") as test_file:
            test_file.write(file_content)

        args = ["cut", "1,3", "test_file.txt"]
        expected_output = "abc\nhij\n"

        Cut.exec(args, [])
        with self.subTest():
            with open("test_file.txt", "r") as test_file:
                self.assertEqual(
                    test_file.readlines(), expected_output.splitlines()
                )

    def test_cut_with_invalid_byte_range(self):
        args = ["cut", "invalid_range", "-"]
        with self.assertRaises(Exception) as context:
            Cut.exec(args, [])
        expected_error_message = "cut: Invalid byte range format"
        self.assertIn(expected_error_message, str(context.exception))

    def test_read_input_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            Cut.read_input("nonexistent_file.txt")

    def test_read_input_generic_error(self):
        with patch("builtins.open", side_effect=Exception("Generic error")):
            with self.assertRaises(Exception):
                Cut.read_input("some_file.txt")

    def test_parse_arguments_index_error(self):
        with self.assertRaises(ValueError) as context:
            Cut.parse_arguments([])

        self.assertIn("No byte range specified", str(context.exception))

    def test_extract_bytes_binary_data(self):
        with self.assertRaises(Exception):
            Cut.extract_bytes("text data", [(1, 5)], is_binary=True)

    def test_extract_bytes_text_data(self):
        with self.assertRaises(Exception) as context:
            Cut.extract_bytes(b"binary data", [(1, 5)], is_binary=False)

        self.assertIn("Error processing data:", str(context.exception))

    def test_read_input_file_open_error(self):
        file_name = "nonexistent_file.txt"

        # Mock the builtins.open function to simulate a file opening error
        with patch(
            "builtins.open", side_effect=IOError("Mocked file open error")
        ):
            with self.assertRaises(Exception):
                Cut.read_input([file_name])

    def test_parse_arguments_invalid_byte_range(self):
        with self.assertRaises(ValueError) as context:
            args = ["cu--t", "inva--lid_range", "file.txt"]
            Cut.parse_arguments(args)

        expected_error_message = "Invalid byte range format"
        self.assertEqual(str(context.exception), expected_error_message)
