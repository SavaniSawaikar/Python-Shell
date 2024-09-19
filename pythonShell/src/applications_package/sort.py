"""
Sort Application
================

This class represents sorting lines of text in files or from standard input.

It reads text from a file specified in the arguments or from standard input,
sorts the lines, and appends them to the output list.
The sorting can be reversed using a command line option.

It follows the format:
    sort [-r] [FILE]...

    - `FILE`(s) is the name(s) of the file(s) to read from.
    - If no files are specified, uses stdin.
    - If the '-r' option is specified, the lines are sorted in reverse order.

Methods:
    exec(args, out): Parses command line arguments, reads input,
                     sorts lines, and appends to output.

Args:
    args (list or str): Command line arguments for the sort utility.
                        If a single argument is passed,
                        it's converted to a list.
                        It supports a '-r' option for reverse sorting.
    out (list): A list where sorted lines of text are appended.

Raises:
    getopt.GetoptError: If there are issues in command line option parsing.
    ValueError: If an invalid command line option is encountered.
    CustomIOError: If there's an IOError while reading from a file.
"""

import sys
import getopt
import os

from custom_errors.customIOError import CustomIOError


class Sort:
    @staticmethod
    def exec(args, out):
        if not isinstance(args, list):
            args = [args]
        args = [arg for arg in args if arg != ""]
        reverse = False
        # parse options
        try:
            opts, args = getopt.getopt(args, "r")
        except getopt.GetoptError as err:
            raise getopt.GetoptError(f"sort: {err}")

        for o, a in opts:
            if o == "-r":
                reverse = True
            else:
                raise ValueError(f"sort: invalid option -- '{o}'")

        lines = []
        if len(args) > 0:
            if os.path.exists(args[0]):
                try:
                    with open(args[0], "r") as f:
                        lines = f.readlines()
                except IOError as e:
                    raise CustomIOError(args[0], e)
            else:
                lines = args
        else:
            lines = sys.stdin.readlines()

        lines.sort(reverse=reverse)

        for line in lines:
            out.append(line.rstrip("\n") + "\n")

        return 0
