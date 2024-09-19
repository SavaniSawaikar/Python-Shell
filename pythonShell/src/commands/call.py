"""
Call Command
==================

This class handles the execution of an application command along with
any necessary argument processing, including input/output redirection,
globbing for wildcard characters in arguments, and handling nested
command calls or pipelines.

Attributes:
    app (str): The name of the application to be executed.
    args (str or list): The arguments to be passed to the application.

Methods:
    eval(output): Evaluates the command, handling redirections,
                    globbing, and command execution.
    _handle_output_redirection(output): Handles output redirection for
                                        the command.
    _handle_input_redirection(output): Handles input redirection for
                                        the command.
    _execute_app(output): Executes the application with processed arguments.
    _perform_globbing(args): Expands arguments using globbing if
                                necessary.
    _is_quoted(string): Checks if a given string is enclosed in quotes.
    _write_to_file(file_name, output): Writes the output to a specified file.
    _read_from_file(file_name, output): Reads input from a specified file.

Raises:
    CommandExecutionError: If the application is not found, or if
                            there's an issue with syntax or file operations.
"""

import commands as commands
import glob
from custom_errors.customCommandExecution import CommandExecutionError
from applications import Application_Factory


class Call(commands.Command):
    def __init__(self, app, args):
        self.app = app
        self.args = args

    def eval(self, output):
        if not self.app:
            raise CommandExecutionError(f"App '{self.app}' not found")

        if isinstance(self.args, (Call, commands.Pipe)):
            self.args.eval(output)
            return

        if ">" in self.args:
            self._handle_output_redirection(output)
        elif "<" in self.args:
            self._handle_input_redirection(output)
        else:
            self._execute_app(output)

    def _handle_output_redirection(self, output):
        redirection_index = self.args.find(">")
        file_name = self.args[redirection_index + 1:].strip()

        self._write_to_file(file_name.strip(), output)

    def _handle_input_redirection(self, output):
        args = self.args.split("<")
        if len(args) != 2:
            raise CommandExecutionError("Invalid syntax")

        self._read_from_file(args[1].strip(), output)

    def _execute_app(self, output):
        app_handler = Application_Factory.get_app(app_name=self.app)
        if app_handler:
            expanded_args = self.args

            if self.app != "find":
                expanded_args = self._perform_globbing(self.args)

            app_handler.exec(expanded_args, output)
        else:
            raise CommandExecutionError(f"App '{self.app}' not found")

    def _perform_globbing(self, args):
        if isinstance(args, list):
            args = " ".join(args)
        args = args.split(" ")

        expanded_args = []
        for arg in args:
            if "*" in arg and not self._is_quoted(arg):
                matched_files = glob.glob(arg)
                if matched_files:
                    expanded_args.extend(matched_files)
                else:
                    expanded_args.append(arg)
            else:
                expanded_args.append(arg)

        return expanded_args

    def _is_quoted(self, string):
        return (
            string.startswith("'")
            and string.endswith("'")
            or string.startswith('"')
            and string.endswith('"')
        )

    def _write_to_file(self, file_name, output):
        if not file_name:
            raise CommandExecutionError("Invalid syntax")

        with open(file_name, "w") as f:
            app_handler = Application_Factory.get_app(app_name=self.app)
            if app_handler:
                args = self.args.replace(">", "").replace(file_name, "")
                f.write(app_handler.exec(args, output))
                output.clear()
            else:
                raise CommandExecutionError(f"App '{self.app}' not found")

    def _read_from_file(self, file_name, output):
        if not file_name:
            raise CommandExecutionError("Invalid syntax")

        app_handler = Application_Factory.get_app(app_name=self.app)
        if app_handler:
            app_handler.exec(file_name, output)
        else:
            raise CommandExecutionError(f"App '{self.app}' not found")
