from rest_framework.exceptions import APIException

class ABDMBaseException(Exception):
    """Base exception for all ABDM-related errors."""
    pass

class ABDMExternalException(ABDMBaseException):
    """Raised for errors from the ABDM external service."""
    def __init__(self, message, url=None, status_code=None, response_body=None, context=None):
        super().__init__(message)
        self.url = url
        self.status_code = status_code
        self.response_body = response_body
        self.context = context

    def __str__(self):
        base = super().__str__()
        return (f"{base} (Context: {self.context}, URL: {self.url}, "
                f"Status: {self.status_code}, Response: {self.response_body})")

class ABDMInternalException(ABDMBaseException):
    """Raised for internal errors in ABDM logic."""
    pass 