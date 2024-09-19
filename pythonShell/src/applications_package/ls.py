"""
Ls Application
==============

This static method mimics the behavior of the Unix 'ls' command.
It lists all non-hidden files and directories in a given directory.
If no directory is specified, it lists the contents of
the current working directory.
Hidden files (those starting with '.') are excluded.

It follows the format:
    ls [DIR]

    - `DIR` is the path to the directory to list.
    - If no directory is specified, uses the current working directory.

Parameters:
args (list): A list of command line arguments.
                This should contain either no elements
                (defaulting to the current working directory)
                or exactly one element
                (the path of the directory to list).
out (list): A list where the output
            (names of files and directories) will be appended.
            Each entry is followed by a newline character.

Raises:
ValueError: If the number of arguments is not 0 or 1.
CustomDirectoryNotFoundError: If the specified directory does not exist.
CustomNotADirectoryError: If the specified path is not a directory.

We use custom exceptions to handle specific error cases.
"""

import os
from os import listdir

from custom_errors.customDirectoryNotFoundError import (
    CustomDirectoryNotFoundError,
)
from custom_errors.customNotADirectoryError import CustomNotADirectoryError


class Ls:
    @staticmethod
    def exec(args, out):
        args = [arg for arg in args if arg != ""]
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ValueError("Wrong number of command line arguments")
        else:
            ls_dir = args[0]

        try:
            for f in listdir(ls_dir):
                if not f.startswith("."):
                    out.append(f + "\n")
        except FileNotFoundError:
            raise CustomDirectoryNotFoundError(ls_dir)
        except NotADirectoryError:
            raise CustomNotADirectoryError(ls_dir)
