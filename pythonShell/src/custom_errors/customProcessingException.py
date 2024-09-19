class CustomProcessingException(Exception):
    """Custom exception class for errors during information processing"""

    def __init__(self, message):
        super().__init__(f"Error processing data: {message}")
