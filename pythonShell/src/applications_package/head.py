"""
Head Application
================

This class is designed to display the first N lines of a given file.
If the number of lines is not specified,
a default of 10 lines is used. It handles file-related errors
by raising custom exceptions.

It follows the format:
    head [-n NUM_LINES] FILE

    - `NUM_LINES` is the number of lines to display.
    - `FILE` is the name of the file to read from.

Static Method:
    exec(args, out): Executes the 'head' command with the provided arguments.

Raises:
    ValueError: If the number of command line
                arguments is incorrect or if the line count
                is not a valid number.
    CustomFileNotFoundError: If the specified file is not found.
    CustomFileException: For other file-related exceptions during file reading.
"""

from custom_errors.customFileException import CustomFileException
from custom_errors.customFileNotFoundError import CustomFileNotFoundError


class Head:
    @staticmethod
    def exec(args, out):
        if not isinstance(args, list):
            args = [args]

        if len(args) != 1 and len(args) != 3:
            raise ValueError("Wrong number of command line arguments")

        num_lines = 10  # Default number of lines
        file = args[0] if len(args) == 1 else args[2]

        if len(args) == 3:
            if args[0] != "-n":
                raise ValueError("Expected '-n' flag for line count")
            try:
                num_lines = int(args[1])
            except ValueError:
                raise ValueError("Line count must be a number")

        try:
            with open(file) as f:
                lines = f.readlines()
                for i in range(min(num_lines, len(lines))):
                    out.append(lines[i])
        except FileNotFoundError:
            raise CustomFileNotFoundError(file)
        except Exception as e:
            raise CustomFileException(file, e)
