class CommandExecutionError(Exception):
    """Custom exception class for errors during command execution."""

    def __init__(self, message, command=None, output=None):
        super().__init__(message)
        self.message = message
        self.command = command
        self.output = output

    def __str__(self):
        if self.command:
            return f"Error executing '{self.command}':\
                {self.message}\nOutput: {self.output}"
        return f"Error: {self.message}\nOutput: {self.output}"
