"""
Echo Application
================

This class is responsible for echoing the provided arguments to the output,
mimicking the behavior of the Unix 'echo' command. It concatenates the
arguments into a single string and appends it to the output list.

It follows the format:
    echo [ARG]...

    - `ARG`(s) is the argument(s) to echo.

Static Methods:
    exec(args, out): Executes the 'echo' command with the provided arguments.
"""


class Echo:
    @staticmethod
    def exec(args, out):
        if not isinstance(args, list):
            args = [args]

        # Join the arguments and append to the output
        out.append(" ".join(args) + "\n")
        string = "".join(args).replace("\n", "")
        return string
