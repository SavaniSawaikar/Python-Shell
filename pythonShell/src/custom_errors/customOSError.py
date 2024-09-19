class CustomOSError(OSError):
    """Custom exception class for OS errors involving directories"""

    def __init__(self, directory, original_error):
        super().__init__(
            f"Error changing to directory '{directory}': {original_error}"
        )
