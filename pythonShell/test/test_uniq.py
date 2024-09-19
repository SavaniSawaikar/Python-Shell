import io
import unittest
from collections import deque
from unittest.mock import mock_open, patch
from applications_package import Uniq
from applications_package.uniq_i import Uniq_i
from shell import eval


class UniqTest(unittest.TestCase):
    def test_uniq_default_behavior(self):
        out = deque()
        input_text = "apple\norange\nbanana\napple\n"
        Uniq.exec([], out, input_stream=input_text.splitlines())

    def test_uniq_with_file(self):
        out = deque()
        input_text = "apple\norange\nbanana\napple\n"
        with open("test_file.txt", "w") as f:
            f.write(input_text)

        Uniq.exec(["test_file.txt"], out)
        out = [part.replace("\n", "") for part in out]
        expected_output = "apple\norange\nbanana\napple\n"
        self.assertEqual(out, deque(expected_output.splitlines()))

    def test_uniq_with_inline_text(self):
        out = deque()
        input_text = "apple\norange\nbanana\napple\n"
        Uniq.exec(
            ["inline", "text"], out, input_stream=input_text.splitlines()
        )

    def test_uniq_with_invalid_file(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            Uniq.exec(["nonexistent_file.txt"], out)

        # Clean up

    def test_uniq(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("uniq 2 3 ", out)

    def test_uniq_no_arguments(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("uniq", out)

    def test_uniq_2_arguments(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("uniq i1 n", out)

    @patch("builtins.open", side_effect=Exception("Error reading file"))
    def test_uniq_exception_reading_file(self, mock_open):
        out = []
        args = ["test_file.txt"]

        with self.assertRaises(Exception):
            Uniq.exec(args, out)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="line1\nline2\nline2\nline3\n",
    )
    def test_uniq_file_reading(self, mock_open):
        out = []
        args = ["test_file.txt"]

        Uniq.exec(args, out)

        expected_output = ["line1\n", "line2\n", "line3\n"]
        self.assertEqual(out, expected_output)

    def test_uniq_nonexistent_file(self):
        out = deque()

        with self.assertRaises(FileNotFoundError):
            eval("uniq non_existent_file.txt", out)

    def test_uniq_invalid_arguments(self):
        out = deque()

        with self.assertRaises(ValueError):
            eval("uniq file1.txt file2.txt", out)

    @patch("builtins.print")
    def test_uniq_with_valid_file(self, mock_print):
        # Test with a valid file
        input_data = "apple\norange\napple\nbanana\n"
        expected_output = "apple\norange\nbanana\n"

        with patch(
            "builtins.open",
            new_callable=open,
            return_value=io.StringIO(input_data),
        ):
            eval("uniq test_file.txt", [])

        mock_print.assert_called_with([expected_output])

    @patch("builtins.print")
    def test_uniq_with_empty_file(self, mock_print):
        # Test with an empty file
        input_data = ""
        expected_output = ""

        with patch(
            "builtins.open",
            new_callable=open,
            return_value=io.StringIO(input_data),
        ):
            eval("uniq test_file.txt", [])

        mock_print.assert_called_with([expected_output])

    def test_uniq_with_nonexistent_file(self):
        # Test with a nonexistent file
        with self.assertRaises(FileNotFoundError):
            eval("uniq nonexistent_file.txt", [])

    def test_uniq_with_invalid_argument_count(self):
        # Test with an invalid number of arguments
        with self.assertRaises(ValueError):
            eval("uniq", [])

    def test_uniq_with_file_reading_error(self):
        # Test with a general file reading error
        with patch(
            "builtins.open", side_effect=Exception("File reading error")
        ):
            with self.assertRaises(Exception) as context:
                eval("uniq test_file.txt", [])

        self.assertIn(
            "Error reading file 'test_file.txt': File reading error",
            str(context.exception),
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="apple\norange\napple\nbanana\n",
    )
    def test_uniq_line_processing(self, mock_file):
        out = []

        eval("uniq test_file_repeated_lines.txt", out)

        mock_file.assert_called_once_with("test_file_repeated_lines.txt")

        # self.assertEqual(out, ["apple\n", "orange\n", "banana\n"])

    def test_exec_wrong_argument_type(self):
        with self.assertRaises(Exception):
            Uniq.exec("not_a_list", [])

    def test_exec_empty_argument_list(self):
        out = []
        Uniq.exec([], out)

    def test_exec_handle_i_option(self):
        with patch.object(Uniq_i, "execs") as mock_execs:
            Uniq.exec(["-i", "file.txt"], [])
            mock_execs.assert_called_once_with(["file.txt"], [])

    def test_exec_read_from_stdin(self):
        with patch("sys.stdin", ["line1", "line2"]):
            out = []
            Uniq.exec([], out)
            self.assertEqual(out, ["line1\n", "line2\n"])

    @patch("builtins.open", mock_open(read_data="line1\nline2\n"))
    def test_exec_process_file(self, mock_open):
        out = []
        Uniq.exec(["file.txt"], out)
        self.assertEqual(out, ["line1\n", "line2\n"])

    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_exec_file_not_found_error(self, mock_open):
        with self.assertRaises(FileNotFoundError) as context:
            Uniq.exec(["nonexistent_file.txt"], [])

        self.assertIn(
            "File 'nonexistent_file.txt' not found", str(context.exception)
        )

    @patch("builtins.open", side_effect=IOError("Error reading file"))
    def test_exec_error_reading_file(self, mock_open):
        with self.assertRaises(Exception):
            Uniq.exec(["file.txt"], [])

    def test_exec_process_inline_text(self):
        out = []
        Uniq.exec(["line1", "line2"], out)
        self.assertEqual(out, ["line1\n", "line2\n"])
