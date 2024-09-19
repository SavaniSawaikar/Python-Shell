"""
Uniq_i Application
==================

This is a class providing functionality similar
to the'uniq' application with case-insensitivity.

It reads text from a file or standard input,
filters out consecutive duplicate lines (ignoring case),
and appends the unique lines to the output list.

It follows the format:

    uniq_i [FILE]...

    - `FILE`(s) is the name(s) of the file(s) to read from.
    - If no files are specified, uses stdin.

Methods:
    execs(args, out):
        Processes the input based on provided
        arguments and appends unique lines to the output.
    _process_input(input_stream, out):
        Helper method to process the input stream
        and filter out consecutive duplicate lines.

Raises:
    CustomFileNotFoundError: If the specified file is not found.
    CustomFileException:
        For any other exceptions encountered while
        processing the file.
"""

import sys
import os

from custom_errors.customFileException import CustomFileException
from custom_errors.customFileNotFoundError import CustomFileNotFoundError


class Uniq_i:
    @staticmethod
    def execs(args, out):
        if not isinstance(args, list):
            args = [args]

        args = [arg for arg in args if arg != ""]

        # If no arguments are provided, read from stdin
        if len(args) == 0:
            Uniq_i._process_input(sys.stdin, out)
            return

        # Check if the argument is a file or inline text
        file_or_text = args[0]
        if os.path.isfile(file_or_text):
            try:
                with open(file_or_text) as f:
                    Uniq_i._process_input(f, out)
            except FileNotFoundError:
                raise CustomFileNotFoundError(file_or_text)
            except Exception as e:
                raise CustomFileException(file_or_text, e)
        else:
            # Treat the argument as inline text
            Uniq_i._process_input(args, out)

    @staticmethod
    def _process_input(input_stream, out):
        input_stream = [
            line
            for item in input_stream
            for line in item.split("\n")
            if line != ""
        ]
        previous_line = None

        for line in input_stream:
            # Remove trailing newline for comparison
            line = line.rstrip("\n")

            # Compare lines in a case-insensitive manner
            # and only add non-duplicate lines
            if previous_line is None or line.lower() != previous_line.lower():
                out.append(line + "\n")  # Append line with newline
                previous_line = line
