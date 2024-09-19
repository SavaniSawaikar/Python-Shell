"""
Uniq Application
================

This is a class providing functionality similar to the Unix 'uniq'.

It reads text from a file or standard input,
filters out consecutive duplicate lines,
and appends the unique lines to the output list.
It supports a case-insensitive mode using the '-i' option.

It follows the format:

        uniq [-i] [FILE]...

        - `FILE`(s) is the name(s) of the file(s) to read from.
        - If no files are specified, uses stdin.
        - If the '-i' option is specified,
          the lines are compared in a case-insensitive manner.

Methods:
    exec(args, out): Processes the input based on
                    provided arguments and appends
                    unique lines to the output.
    _process_input(input_stream, out):
                    Helper method to process the
                    input stream and filter out
                    consecutive duplicate lines.

Raises:
    CustomFileNotFoundError: If the specified file is not found.
    CustomFileException: For any other exceptions
                        encountered while processing the file.
"""

import os
import sys
from .uniq_i import Uniq_i
from custom_errors.customFileException import CustomFileException
from custom_errors.customFileNotFoundError import CustomFileNotFoundError


class Uniq:
    @staticmethod
    def exec(args, out):
        if not isinstance(args, list):
            args = [args]

        args = [arg for arg in args if arg != ""]

        # Handling the -i option
        if args[0] == "-i":
            Uniq_i.execs(args[1:], out)
            return

        # If no arguments are provided, read from stdin
        if len(args) == 0:
            Uniq._process_input(sys.stdin, out)
            return

        # Check if the argument is a file or inline text
        file_or_text = args[0]
        if os.path.isfile(file_or_text):
            try:
                with open(file_or_text) as f:
                    Uniq._process_input(f, out)
            except FileNotFoundError:
                raise CustomFileNotFoundError(file_or_text)
            except Exception as e:
                raise CustomFileException(file_or_text, e)
        else:
            # Treat the argument as inline text
            Uniq._process_input(args, out)

    @staticmethod
    def _process_input(input_stream, out):
        previous_line = None
        for line in input_stream:
            if not line.endswith("\n"):
                line += "\n"

            if previous_line is None or line != previous_line:
                # Append the original line, not the trimmed line
                out.append(line)
                previous_line = line
