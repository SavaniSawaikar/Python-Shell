"""
Grep Application
================

This class is designed to search for lines in given files (or standard input)
that match a specified pattern.
It supports regular expressions for pattern matching
and can handle multiple file inputs.

It follows the format:
    grep PATTERN [FILE]...

    - `PATTERN` is the pattern to match against.
    - `FILE`(s) is the name(s) of the file(s) to read from.
    - If no files are specified, uses stdin.

Static Method:
    exec(args, out): Executes the 'grep' command with the provided arguments.

Raises:
    ValueError: If the number of command line arguments is incorrect.
    CustomFileNotFoundError: If a specified file is not found.
    CustomFileException: For other file-related exceptions during file reading.
"""

import re
import os

from custom_errors.customFileException import CustomFileException
from custom_errors.customFileNotFoundError import CustomFileNotFoundError


class Grep:
    @staticmethod
    def exec(args, out):
        if len(args) < 2:
            raise ValueError("Wrong number of command line arguments")

        pattern = args[0]
        inputs = args[1:]

        pattern = pattern.replace("'", "")

        # Check if all inputs are from the same file
        all_from_same_file = (
            all(os.path.isfile(input) for input in inputs)
            and len(set(inputs)) == 1
        )

        for input in inputs:
            if os.path.isfile(input):
                # If the input is a file path, read from the file
                try:
                    with open(input) as f:
                        lines = f.readlines()
                except FileNotFoundError:
                    raise CustomFileNotFoundError(input)
                except Exception as e:
                    raise CustomFileException(input, e)
            else:
                # If the input is a direct string, consider it as a single line
                lines = [input]

            # Perform the grep operation on each line
            for line in lines:
                if not line.endswith("\n"):
                    line += "\n"
                if re.search(pattern, line):
                    # Append the line with or without filename
                    # based on the condition
                    formatted_line = (
                        f"{input}:{line}"
                        if os.path.isfile(input) and not all_from_same_file
                        else line
                    )
                    out.append(formatted_line)
