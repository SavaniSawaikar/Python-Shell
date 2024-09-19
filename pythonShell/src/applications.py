"""
Application Factory
===================
Factory class to create instances of command applications.

This class serves as a central point for obtaining instances of various
command applications, both in their standard and safe (error-handling)
versions. It uses a registry pattern to maintain a mapping between command
names and their corresponding classes.

Attributes:
    registry (dict): A dictionary mapping application names to their classes.
"""

from applications_package import (
    Cd,
    Echo,
    Pwd,
    Ls,
    Cat,
    Head,
    Tail,
    Grep,
    Find,
    Uniq,
    Cut,
    Sort,
    Uniq_i,
)

from safe_application_decorator import SafeApplication


class Application_Factory:
    registry = {
        "echo": Echo,
        "pwd": Pwd,
        "cd": Cd,
        "head": Head,
        "cat": Cat,
        "ls": Ls,
        "tail": Tail,
        "grep": Grep,
        "find": Find,
        "uniq": Uniq,
        "uniq-i": Uniq_i,
        "cut": Cut,
        "sort": Sort,
    }

    @staticmethod
    def get_app(app_name):
        if app_name in Application_Factory.registry:
            app_class = Application_Factory.registry[app_name]
            # Return the original application
            return app_class

        # Check if the requested app is an unsafe version
        elif app_name.startswith("_"):
            # Return the safe decorated version of the application
            safe_app_name = app_name[
                1:
            ]  # Remove underscore to get the safe version's name
            safe_app_class = Application_Factory.registry[safe_app_name]
            return SafeApplication(safe_app_class)

        else:
            raise ValueError(f"Unsupported application {app_name}")
