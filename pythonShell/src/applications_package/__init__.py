"""This is the applications package and makes the factory design pattern easier
to implement when importing all the application classes."""

from .cat import Cat
from .cd import Cd
from .echo import Echo
from .grep import Grep
from .head import Head
from .ls import Ls
from .pwd import Pwd
from .tail import Tail
from .find import Find
from .uniq import Uniq
from .cut import Cut
from .sort import Sort
from .uniq_i import Uniq_i


# This is to avoid linting errors about unused imports,
# since these imports are used in other files.

__all__ = [
    "Cat",
    "Cd",
    "Echo",
    "Grep",
    "Head",
    "Ls",
    "Pwd",
    "Tail",
    "Find",
    "Uniq",
    "Cut",
    "Sort",
    "Uniq_i",
]
