"""
Find Application
================

This class is designed to search for files in a specified directory that match
a given pattern.
It supports wildcards and regular expressions for pattern matching.

It follows the format:
    find PATH -name PATTERN

    - `PATH` is the path to the directory to search in.
    - `PATTERN` is the pattern to match against.

Static Method:
    exec(args, out): Executes the 'find' command with the provided arguments.

Raises:
    ValueError: If the usage is incorrect.
    CustomDirectoryNotFoundError:
    If the specified directory does not exist or is not a directory.
"""

import re
from pathlib import Path

from custom_errors.customDirectoryNotFoundError import (
    CustomDirectoryNotFoundError,
)


class Find:
    @staticmethod
    def exec(args, out):
        if len(args) < 2:
            raise ValueError("Usage: find [PATH] -name PATTERN")

        if not isinstance(args, list):
            args = args.split(" ")

        # Extract pattern and path from args
        pattern_index = args.index("-name") + 1
        if pattern_index >= len(args):
            raise ValueError("Pattern not specified after -name")

        pattern = args[pattern_index].replace("*", ".*")
        pattern = pattern.replace("'", "")
        path = Path(args[0]) if args[0] != "-name" else Path(".")

        if not path.exists() or not path.is_dir():
            raise CustomDirectoryNotFoundError(path)

        regex = re.compile(pattern)

        try:
            for file in path.glob("**/*"):
                if file.is_file() and regex.match(file.name):
                    relative_path = str(file.relative_to("."))
                    if path.absolute() == Path(".").absolute():
                        relative_path = "./" + relative_path
                    out.append(relative_path + "\n")
        except re.error:
            raise ValueError(f"Invalid regular expression: '{pattern}'")
