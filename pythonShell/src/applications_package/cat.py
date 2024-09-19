"""
Cat Application
===============

This class is responsible for concatenating and displaying the contents
of files provided as arguments. If no file names are provided, it reads
from standard input.

It follows the format:
    cat [FILE]...

    - `FILE`(s) is the name(s) of the file(s) to contatenate.
    - If no files are specified, uses stdin.

The class uses custom exceptions to handle file-related errors, ensuring
more descriptive error messages are provided to the user.

Methods:
    exec(args, out): Executes the 'cat' command with the provided arguments.
"""


import sys
from custom_errors.customFileNotFoundError import CustomFileNotFoundError
from custom_errors.customFileException import CustomFileException


class Cat:
    @staticmethod
    def exec(args, out):
        # Check if args is a list; if not, convert it to a list
        if not isinstance(args, list):
            args = [args]

        args = [arg for arg in args if arg != ""]

        # If args is empty, read from stdin
        if not args:
            out.extend(sys.stdin.readlines())
        else:
            # Process each file in args
            for filename in args:
                try:
                    with open(filename, "r") as file:
                        for line in file:
                            if "\n" not in line:
                                line += "\n"
                            out.append(line)

                except FileNotFoundError:
                    raise CustomFileNotFoundError(filename)
                except Exception as e:
                    raise CustomFileException(filename, e)
