"""
Pwd Application
===============

This static method simulates the behavior of the Unix 'pwd' command,
which prints the path of the current working directory.
The result is appended to the provided output list,
each followed by a newline character.

It follows the format:
    pwd

Parameters:
args (list): A list of command line arguments.
             For the 'pwd' command, this list should
            be empty as no arguments are needed.
out (list): A list where the output
            (the current working directory path) will be appended.
            Each entry is followed by a newline character.

Raises:
OSError: If an error occurs during the retrieval
         of the current working directory.
        The error message is formatted to
        provide detailed information about the issue.


This is designed to work without any arguments,
and will raise an exception if it encounters
issues accessing the directory information.
"""

import os


class Pwd:
    @staticmethod
    def exec(args, out):
        try:
            out.append(os.getcwd() + "\n")
        except OSError as e:
            raise OSError(f"Error retrieving current directory: {e}")
