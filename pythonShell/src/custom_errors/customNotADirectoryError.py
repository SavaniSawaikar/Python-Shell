class CustomNotADirectoryError(NotADirectoryError):
    """Custom exception class for Not A Directory errors"""

    def __init__(self, directory):
        super().__init__(f"'{directory}' is not a directory.")
