from rest_framework.exceptions import APIException

class ABDMBaseException(Exception):
    """Base exception for all ABDM-related errors."""
    pass

class ABDMExternalException(ABDMBaseException):
    """Raised for errors from the ABDM external service."""
    def __init__(self, message, url=None, status_code=None, response_body=None, context=None):
        """
        Initialize an ABDMExternalException with details about an external ABDM service error.
        
        Parameters:
            message (str): Description of the error.
            url (str, optional): The URL of the external request that caused the error.
            status_code (int, optional): HTTP status code returned by the external service.
            response_body (str, optional): Response body from the external service.
            context (dict, optional): Additional context or metadata related to the error.
        """
        super().__init__(message)
        self.url = url
        self.status_code = status_code
        self.response_body = response_body
        self.context = context

    def __str__(self):
        """
        Return a string representation of the exception, including the message, context, URL, HTTP status code, and response body.
        """
        base = super().__str__()
        return (f"{base} (Context: {self.context}, URL: {self.url}, "
                f"Status: {self.status_code}, Response: {self.response_body})")

class ABDMInternalException(ABDMBaseException):
    """Raised for internal errors in ABDM logic."""
    pass 