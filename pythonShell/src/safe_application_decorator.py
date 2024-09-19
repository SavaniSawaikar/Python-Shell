"""
This is a wrapper class for safely executing methods of an application.

This class is designed to encapsulate an application object and provides a safe
execution environment for its methods.
It primarily focuses on handling exceptions
that may arise during the execution of the application's methods.

Attributes:
    application (object): An instance of the application that
                          this class will manage.

Methods:
    __init__(application: object)
        Initializes the SafeApplication instance
        with the given application object.

Instantiation:
application (object): The application instance that will
                      be managed by this class.

exec(args: List[str], out: List[str])
Executes the `exec` method of the encapsulated application, safely handling
any exceptions that arise. In the case of an exception, the error message is
appended to the provided output list.

Parameters:
args (List[str]): A list of arguments to pass to the application's
                `exec` method.
out (List[str]): A list where the output or error messages will be appended.
"""


class SafeApplication:
    def __init__(self, application):
        self.application = application

    def exec(self, args, out):
        try:
            self.application.exec(args, out)
        except Exception as error:
            out.append(f"{error}\n")
