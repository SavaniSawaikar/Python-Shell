import unittest
from collections import deque
from shell import eval
import os
from unittest.mock import patch


class CdTest(unittest.TestCase):
    def test_cd_valid_directory(self):
        out = deque()
        valid_directory = os.path.dirname(os.path.abspath(__file__))
        eval(f"cd {valid_directory}", out)
        self.assertEqual(os.getcwd(), valid_directory)

    def test_cd_invalid_directory(self):
        out = deque()
        invalid_directory = "/nonexistent/directory"
        with self.assertRaises(FileNotFoundError):
            eval(f"cd {invalid_directory}", out)

    # def test_cd_not_a_directory(self):
    #     out = deque()
    #     with NamedTemporaryFile() as tmpfile:
    #         test_file = tmpfile.name
    #         with self.assertRaises(NotADirectoryError):
    #             eval(f'cd {test_file}', out)

    @patch("os.chdir")
    def test_cd_oserror(self, mock_chdir):
        mock_chdir.side_effect = OSError("Mocked OSError")
        test_directory = "/some/directory"
        out = deque()
        with self.assertRaises(OSError) as context:
            eval(f"cd {test_directory}", out)
        self.assertEqual(
            str(context.exception),
            f"Error changing to directory '{test_directory}': Mocked OSError",
        )

    def test_cd_multi(self):
        out = deque()
        with self.assertRaises(ValueError):
            eval("cd dir1 dir2", out)

    # def test_cd_directory_not_found(self):
    #     out = deque()
    #     with self.assertRaises(FileNotFoundError) as context:
    #         eval("cd .txt", out)

    @patch(
        "os.chdir"
    )  # Mock the os.chdir function to avoid actual directory changes
    def test_cd_directory_success(self, mock_chdir):
        # Arrange
        out = deque()

        # Act
        eval("cd valid_directory", out)

        # Assert
        mock_chdir.assert_called_once_with("valid_directory")
        self.assertEqual(
            len(out), 0
        )  # Ensure out is empty as no error message should be appended

    @patch("os.chdir")
    def test_cd_directory_not_found(self, mock_chdir):
        # Arrange
        out = deque()
        mock_chdir.side_effect = FileNotFoundError("Directory not found")

        # Act and Assert
        with self.assertRaises(FileNotFoundError) as context:
            eval("cd non_existent_directory", out)

        self.assertEqual(
            str(context.exception),
            "Directory 'non_existent_directory' not found",
        )
        mock_chdir.assert_called_once_with(
            "'not_a_directory' is not a directory."
        )

        self.assertEqual(len(out), 0)

    @patch("os.chdir")
    def test_cd_not_a_directory(self, mock_chdir):
        # Arrange
        out = deque()
        mock_chdir.side_effect = NotADirectoryError("Not a directory")

        # Act and Assert
        with self.assertRaises(NotADirectoryError) as context:
            eval("cd not_a_directory", out)

        self.assertEqual(
            str(context.exception), "'not_a_directory' is not a directory"
        )

        # Ensure os.chdir was called with the correct argument
        mock_chdir.assert_called_once_with("not_a_directory")

        # Ensure no additional error message is appended to out
        self.assertEqual(len(out), 0)

    @patch("os.chdir")
    def test_cd_os_error(self, mock_chdir):
        # Arrange
        out = deque()
        mock_chdir.side_effect = OSError("Generic OS error")

        # Act and Assert
        with self.assertRaises(OSError) as context:
            eval("cd error_directory", out)

        self.assertTrue(
            str(context.exception).startswith(
                "Error changing to directory 'error_directory'"
            )
        )

        # Ensure os.chdir was called with the correct argument
        mock_chdir.assert_called_once_with("error_directory")

        # Ensure no additional error message is appended to out
        self.assertEqual(len(out), 0)

    def test_unsafe_cd(self):
        out = deque()
        eval("_cd nonfile.txt", out)
        self.assertEqual(out.pop(), "Directory 'nonfile.txt' not found\n")
