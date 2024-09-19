"""
Pipe Command
============

This is a command class representing a pipe operation.

The Pipe class is used to direct the output of one command (left) as the input
to another command (right), mimicking the behavior of a Unix-style pipe.

Attributes:
    left (Command): The command on the left side of the pipe.
    right (Command): The command on the right side of the pipe.

Methods:
    eval(output): Executes the pipe operation
                    by first evaluating the left command,
                    then passing its output as the input to the right command.

Raises:
    CommandExecutionError: If the right command in the pipe is not an instance
                            of the Call class.
"""

import commands as commands
from custom_errors.customCommandExecution import CommandExecutionError
from commands import Call


class Pipe(commands.Command):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, output):
        left_output = []
        self.left.eval(left_output)
        # Assuming each line in left_output is a separate argument
        # for the right command
        right_input = [line.strip() for line in left_output]

        if isinstance(self.right, Call):
            # Prepending the existing arguments of the right command
            #  with the output from the left
            self.right.args = [self.right.args] + right_input
        else:
            raise CommandExecutionError(
                "Right side of pipe is not a call command"
            )

        self.right.eval(output)
