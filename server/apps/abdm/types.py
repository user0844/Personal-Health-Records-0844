from typing import TypedDict

class SessionData(TypedDict):
    """Type declaration for ABDM session data."""
    accessToken: str
    expiresIn: int
    refreshExpiresIn: int
    refreshToken: str
    tokenType: str
    cachedAt: float 