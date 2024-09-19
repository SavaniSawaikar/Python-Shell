class CustomFileNotFoundError(FileNotFoundError):
    """Custom exception class for file not found errors"""

    def __init__(self, filename):
        super().__init__(f"File '{filename}' not found.")
