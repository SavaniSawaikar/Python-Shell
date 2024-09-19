"""
Command
=======

This is an abstract base class representing a command.

This class serves as a template for defining various commands in the system.
Subclasses of Command should implement the specific logic for different types
of command-line operations.

The primary method `eval` is abstract and is overridden in subclasses.
"""

from abc import abstractmethod


class Command:
    @abstractmethod
    def eval(self, output):
        pass
