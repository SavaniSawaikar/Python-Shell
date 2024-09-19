import unittest
from unittest.mock import MagicMock
from custom_errors.customCommandExecution import CommandExecutionError

from commands import Pipe, Call


class PipeTest(unittest.TestCase):

    def test_pipe_with_non_call(self):
        # Set up the test case
        left_command = MagicMock()
        right_command = MagicMock()
        pipe_instance = Pipe(left_command, right_command)

        # Mock the eval method of left_command
        left_command.eval.return_value = ["left_output"]

        # Call the eval method of Pipe, expecting a CommandExecutionError
        output = []
        with self.assertRaises(CommandExecutionError):
            pipe_instance.eval(output)

        # Verify that the left_command.eval method was called
        left_command.eval.assert_called_once_with(["left_output"])

    def test_pipe_with_call_commands(self):
        # Arrange
        left_command = Call("echo", ["hello"])
        right_command = Call("grep", ["e"])
        pipe = Pipe(left_command, right_command)
        output = []

        # Act
        pipe.eval(output)

        # Assert

    def test_pipe_with_empty_left_output(self):
        # Arrange
        left_command = Call("echo", [""])
        right_command = Call("grep", ["e"])
        pipe = Pipe(left_command, right_command)
        output = []
        pipe.eval(output)

    def test_pipe_with_non_call_right_command(self):
        # Arrange
        left_command = Call("echo", ["hello"])
        right_command = Pipe(
            Call("grep", ["e"]), Call("wc", [])
        )  # Using Pipe as a non-Call right command
        pipe = Pipe(left_command, right_command)
        output = []

        # Act and Assert
        with self.assertRaises(CommandExecutionError) as context:
            pipe.eval(output)

        expected_error_message = (
            "Error: Right side of pipe is not a call command\nOutput: None"
        )
        self.assertEqual(str(context.exception), expected_error_message)
