"""
Tail Application
================

This is a class representing a utility for displaying the last part of a file.

It reads a specified number of lines from the end of a file and
appends them to the output list.
The number of lines to be read can be specified through command line arguments.

It follows the format:
    tail [-n NUM_LINES] FILE

    - `NUM_LINES` is the number of lines to display.
    - `FILE` is the name of the file to read from.

Methods:
    exec(args, out): Parses command line arguments,
    reads the specified number of lines from the end of a file,
    and appends them to the output list.

Returns:
    None: Appends the lines to the 'out' list.
    Raises an exception in case of errors.

Raises:
    ValueError: If the number of arguments is incorrect,
                or if the '-n' flag is used incorrectly,
                or if the specified line count is not a number.
    CustomFileNotFoundError: If the specified file is not found.
    CustomFileException: For any other exceptions
                        encountered while processing the file.
"""

from custom_errors.customFileException import CustomFileException
from custom_errors.customFileNotFoundError import CustomFileNotFoundError


class Tail:
    @staticmethod
    def exec(args, out):
        if not isinstance(args, list):
            args = [args]
        # Check the number of arguments
        if (len(args) != 1 and len(args) != 3) or ("" in args):
            raise ValueError("Wrong number of command line arguments")

        # Default number of lines to display
        num_lines = 10

        # Parse arguments
        if len(args) == 1:
            file = args[0]
        if len(args) == 3:
            if args[0] != "-n":
                raise ValueError("Expected '-n' flag for line count")
            try:
                num_lines = int(args[1])
            except ValueError:
                raise ValueError("Line count must be a number")
            file = args[2]

        # Read file and process lines
        try:
            with open(file) as f:
                lines = f.readlines()
                display_length = min(len(lines), num_lines)
                for i in range(len(lines) - display_length, len(lines)):
                    out.append(lines[i])
        except FileNotFoundError:
            raise CustomFileNotFoundError(file)
        except Exception as e:
            raise CustomFileException(file, e)
