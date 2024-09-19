class CustomIOError(IOError):
    """Custom exception class for IO errors during file reading"""

    def __init__(self, filename, error):
        super().__init__(f"Error reading file '{filename}': {error}")
