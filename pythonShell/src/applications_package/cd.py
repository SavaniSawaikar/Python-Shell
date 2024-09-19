"""
Cd application
=================

This class is responsible for changing the current working directory of the
shell to a specified path. It handles various errors related to directory
changes and raises custom exceptions to provide a more descriptive
error messages.

It follows the format:
    cd PATH

    - `PATH` is the path to the directory to change to.

Methods:
    exec(args, out): Executes the 'cd' command with the provided arguments.
"""

import os
from custom_errors.customDirectoryNotFoundError import (
    CustomDirectoryNotFoundError,
)
from custom_errors.customNotADirectoryError import CustomNotADirectoryError
from custom_errors.customOSError import CustomOSError


class Cd:
    @staticmethod
    def exec(args, out):
        # Check the number of arguments
        if len(args) == 0 or len(args) > 1:
            raise ValueError("Wrong number of command line arguments")

        # Change directory
        try:
            os.chdir(args[0])
        except FileNotFoundError:
            raise CustomDirectoryNotFoundError(args[0])
        except NotADirectoryError:
            raise CustomNotADirectoryError(args[0])
        except OSError as e:
            raise CustomOSError(args[0], e)
