import io
import unittest
from collections import deque
import os
from unittest.mock import patch
from applications_package import Uniq_i
from tempfile import NamedTemporaryFile


class UniqTest(unittest.TestCase):
    def test_uniq_i_success(self):
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write("AAA\nAAA\nCCC\n")
            file_name = tmpfile.name

        out = deque()
        args = file_name
        Uniq_i.execs([args], out)

        result = []
        while out:
            result.append(out.popleft())

        expected_result = ["AAA\n", "CCC\n"]
        self.assertEqual(expected_result, result)

        os.remove(file_name)

    def test_uniq_i_valueError(self):
        out = deque()
        args = "file name"

        # Use assertRaises to check for the expected ValueError
        with self.assertRaises(ValueError) as context:
            Uniq_i.execs([args], out)

        # Assert that the error message matches the expected message
        expected_error_message = "Usage: uniq <file>"
        self.assertEqual(expected_error_message, str(context.exception))

    def test_unsafe_uniqi(self):
        out = deque()
        Uniq_i.execs(["_uniq-i nonfile.txt"], out)

    @patch(
        "builtins.open", side_effect=Exception("Simulated file reading error")
    )
    def test_file_exception_handling(self):
        out = deque()
        args = "file_name.txt"

        # Ensure that the Uniq_i.execs method raises the expected exception
        with self.assertRaises(Exception) as context:
            Uniq_i.execs([args], out)

        # Assert that the error message matches the expected message
        expected_error_message = (
            f"Error reading file '{args}': Simulated file reading error"
        )
        self.assertEqual(expected_error_message, str(context.exception))

    def test_uniq_i_process_input_stdin(self):
        out = deque()

        # Patch sys.stdin for testing
        with patch("sys.stdin", new=io.StringIO("stdin content\n")):
            Uniq_i._process_input([], out)

        self.assertEqual(out.popleft(), "stdin content\n")

    def test_uniq_i_process_input_file(self):
        out = deque()
        file_content = "file content\n"
        with NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
            tmpfile.write(file_content)
            file_name = tmpfile.name

        Uniq_i._process_input([file_name], out)

        self.assertEqual(out.popleft(), file_content)

        os.remove(file_name)

    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_uniq_i_process_input_file_not_found(self):
        out = deque()
        with self.assertRaises(FileNotFoundError) as context:
            Uniq_i._process_input(["nonexistent_file.txt"], out)

        self.assertEqual(str(context.exception), "File not found")

    def test_uniq_i_process_input_generic_error(self):
        out = deque()
        with self.assertRaises(Exception) as context:
            Uniq_i._process_input(["test_file.txt"], out)

        self.assertEqual(
            str(context.exception), "Simulated file reading error"
        )
