class CustomDirectoryNotFoundError(FileNotFoundError):
    """Custom exception class for directory not found errors."""

    def __init__(self, directory_name):
        super().__init__(f"Directory '{directory_name}' not found")
