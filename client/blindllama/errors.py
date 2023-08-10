class APIKeyException(Exception):
    """
    A custom exception class for wrapping API Key verification errors
    """

    def __init__(self, key, msg):
        self.key = key
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"
    
class PredictionException(Exception):
    """
    A custom exception class for wrapping predictions errors
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"