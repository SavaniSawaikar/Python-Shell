import unittest
from unittest.mock import create_autospec, patch, Mock, mock_open
from commands import Call
import commands
from custom_errors.customCommandExecution import CommandExecutionError


class CallTest(unittest.TestCase):
    def test_execute_app_success(self):
        call = Call("echo", "Hello World")
        output = Mock()

        call._execute_app(output)

        output.append.assert_called_with("Hello World\n")

    @patch("applications.Application_Factory.get_app", return_value=None)
    def test_execute_app_not_found(self, mock_get_app):
        call = Call("nonexistent_app", "arg1 arg2")
        output = Mock()

        with self.assertRaises(CommandExecutionError) as context:
            call._execute_app(output)

        mock_get_app.assert_called_once_with(app_name="nonexistent_app")
        self.assertEqual(
            str(context.exception),
            "Error: App 'nonexistent_app' not found\nOutput: None",
        )

    @patch("applications.Application_Factory.get_app")
    def test_handle_output_redirection_success(self, mock_get_app):
        mock_app_handler = Mock()
        mock_app_handler.exec = Mock()
        mock_get_app.return_value = mock_app_handler

        call = Call("mock_app", "arg1 arg2 . input.txt")
        output = Mock()

        with patch(
            "builtins.open", mock_open(read_data="input_data")
        ) as mock_file: # noqa F841
            call._handle_output_redirection(output)

    def test_handle_output_redirection_invalid_syntax(self):
        call = Call("mock_app", "arg1 arg2 >")
        output = Mock()

        with self.assertRaises(CommandExecutionError) as context:
            call._handle_output_redirection(output)

        self.assertEqual(
            str(context.exception), "Error: Invalid syntax\nOutput: None"
        )

    @patch("applications.Application_Factory.get_app")
    def test_handle_input_redirection_success(self, mock_get_app):
        mock_app_handler = Mock()
        mock_app_handler.exec = Mock()
        mock_get_app.return_value = mock_app_handler

        call = Call("mock_app", "arg1 arg2 < input.txt")
        output = Mock()

        with patch(
            "builtins.open", mock_open(read_data="input_data")
        ) as mock_file: # noqa F841
            call._handle_input_redirection(output)

    def test_handle_input_redirection_invalid_syntax(self):
        call = Call("mock_app", "arg1 arg2 <")
        output = Mock()

        with self.assertRaises(CommandExecutionError) as context:
            call._handle_input_redirection(output)

        self.assertEqual(
            str(context.exception), "Error: Invalid syntax\nOutput: None"
        )

    @patch("applications.Application_Factory.get_app", return_value=None)
    def test_write_to_file_app_not_found(self, mock_get_app):
        call = Call("nonexistent_app", "arg1 arg2 > output.txt")
        output = Mock()

        with self.assertRaises(CommandExecutionError) as context:
            call._write_to_file("output.txt", output)

        mock_get_app.assert_called_once_with(app_name="nonexistent_app")
        self.assertEqual(
            str(context.exception),
            "Error: App 'nonexistent_app' not found\nOutput: None",
        )

    def test_read_from_file_success(self):
        call = Call("mock_app", "arg1 arg2 < input.txt")
        output = Mock()

        with patch(
            "applications.Application_Factory.get_app",
            return_value=Mock(exec=lambda args, out: "Mocked output"),
        ):
            call._read_from_file("input.txt", output)

    @patch("applications.Application_Factory.get_app", return_value=None)
    def test_read_from_file_app_not_found(self, mock_get_app):
        call = Call("nonexistent_app", "arg1 arg2 < input.txt")
        output = Mock()

        with self.assertRaises(CommandExecutionError) as context:
            call._read_from_file("input.txt", output)

        mock_get_app.assert_called_once_with(app_name="nonexistent_app")
        self.assertEqual(
            str(context.exception),
            "Error: App 'nonexistent_app' not found\nOutput: None",
        )

    def test_perform_globbing_with_globbing(self):
        call = Call("mock_app", "arg1 *.txt arg2")
        expanded_args = call._perform_globbing(call.args)
        expected_expanded_args = ["arg1", "requirements.txt", "arg2"]

        self.assertEqual(expanded_args, expected_expanded_args)

    def test_perform_globbing_without_globbing(self):
        call = Call("mock_app", "arg1 arg2")
        expanded_args = call._perform_globbing(call.args)
        expected_expanded_args = ["arg1", "arg2"]

        self.assertEqual(expanded_args, expected_expanded_args)

    def test_is_quoted_true_single_quotes(self):
        call = Call("mock_app", "arg1 arg2")
        result = call._is_quoted("'quoted_string'")

        self.assertTrue(result)

    def test_is_quoted_true_double_quotes(self):
        call = Call("mock_app", "arg1 arg2")
        result = call._is_quoted('"quoted_string"')

        self.assertTrue(result)

    def test_is_quoted_false(self):
        call = Call("mock_app", "arg1 arg2")
        result = call._is_quoted("unquoted_string")
        self.assertFalse(result)

    @patch(
        "applications.Application_Factory.get_app",
        return_value=Mock(exec=lambda args, out: "Mocked output"),
    )
    def test_eval_app_not_found(self, mock_get_app):
        call = Call(None, "arg1 arg2")
        output = Mock()

        with self.assertRaises(CommandExecutionError) as context:
            call.eval(output)

        mock_get_app.assert_not_called()
        self.assertEqual(
            str(context.exception), "Error: App 'None' not found\nOutput: None"
        )

    @patch("applications.Application_Factory.get_app", return_value=None)
    def test_eval_invalid_app(self, mock_get_app):
        call = Call("invalid_app", "arg1 arg2")
        output = Mock()

        with self.assertRaises(CommandExecutionError) as context:
            call.eval(output)

        mock_get_app.assert_called_once_with(app_name="invalid_app")
        # Update the expected message to match the actual one
        self.assertEqual(
            str(context.exception),
            "Error: App 'invalid_app' not found\nOutput: None",
        )

    @patch("applications.Application_Factory.get_app")
    def test_eval_pipe_instance(self, mock_get_app):
        # Create a mock pipe instance resembling commands.Pipe
        pipe_instance = create_autospec(commands.Pipe)

        call = Call("mock_app", pipe_instance)
        output = Mock()

        call.eval(output)

        pipe_instance.eval.assert_called_once_with(output)
        self.assertEqual(mock_get_app.call_count, 0)
        output.append.assert_not_called()

    @patch("applications.Application_Factory.get_app")
    def test_eval_output_redirection(self, mock_get_app):
        call = Call("mock_app", "arg1 arg2 > output.txt")
        output = Mock()

        with patch.object(
            call, "_handle_output_redirection"
        ) as mock_handle_output:
            call.eval(output)

        mock_handle_output.assert_called_once_with(output)
        self.assertEqual(
            mock_get_app.call_count, 0
        )
        output.append.assert_not_called()

    @patch("applications.Application_Factory.get_app")
    def test_eval_input_redirection(self, mock_get_app):
        call = Call("mock_app", "arg1 arg2 < input.txt")
        output = Mock()

        with patch.object(
            call, "_handle_input_redirection"
        ) as mock_handle_input:
            call.eval(output)

        mock_handle_input.assert_called_once_with(output)
        self.assertEqual(
            mock_get_app.call_count, 0
        )  # Expecting get_app not to be called
        output.append.assert_not_called()

    @patch("applications.Application_Factory.get_app")
    def test_eval_execute_app(self, mock_get_app):
        call = Call("mock_app", "arg1 arg2")
        output = Mock()

        with patch.object(call, "_execute_app") as mock_execute_app:
            call.eval(output)

        mock_execute_app.assert_called_once_with(output)
        self.assertEqual(mock_get_app.call_count, 0)
        output.append.assert_not_called()
