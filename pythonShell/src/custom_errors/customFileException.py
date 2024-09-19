class CustomFileException(Exception):
    """Custom exception class for errors while reading files"""

    def __init__(self, filename, error):
        super().__init__(f"Error reading file '{filename}': {error}")
