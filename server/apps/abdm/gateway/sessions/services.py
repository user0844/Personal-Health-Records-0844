import uuid
import requests
import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from .exceptions import ABDMExternalException, ABDMInternalException
from apps.abdm.types import SessionData

logger = logging.getLogger(__name__)

CACHE_KEY = "abdm_session"

class ABDMSession:
    """
    Manages the ABDM session token by fetching it from the gateway
    and caching it. It provides a single point of access for the token.
    """

    def __init__(self):
        self.client_id = settings.ABDM_CONFIG['CLIENT_ID']
        self.client_secret = settings.ABDM_CONFIG['CLIENT_SECRET']
        self.x_cm_id = settings.ABDM_CONFIG['X_CM_ID']
        self.gateway_base_url = settings.ABDM_CONFIG['GATEWAY_BASE_URL']
        self.session_endpoint = settings.ABDM_CONFIG['SESSIONS_ENDPOINT']
        # Only accept status code 202 as valid
        self.expected_status_code = 202

    def get_session(self) -> SessionData:
        """
        Retrieves the session from the cache, proactively refreshing or creating a new session if needed.

        Returns:
            SessionData: The session data.

        Raises:
            Exception: If the session is not found in the cache.
        """
        session: SessionData = cache.get(CACHE_KEY)

        if not session:
            return self.create_session()
        
        now = timezone.now().timestamp()
        access_token_expiry = session['cachedAt'] + session['expiresIn']
        refresh_token_expiry = session['cachedAt'] + session['refreshExpiresIn']
        buffer_seconds = 180    # 3 minutes buffer
        if access_token_expiry - now < buffer_seconds:
            if refresh_token_expiry > now:
                return self.refresh_session(session['refreshToken'])
            else:
                return self.create_session()
        return session

    def create_session(self) -> SessionData:
        """
        Creates a new session with the ABDM gateway and caches it.

        Returns:
            SessionData: The newly created session data.

        Raises:
            requests.exceptions.RequestException: If the API call fails.
        """
        url = f"{self.gateway_base_url}{self.session_endpoint}"

        headers = {
            'REQUEST-ID': str(uuid.uuid4()),
            'TIMESTAMP': datetime.now().isoformat(),
            'X-CM-ID': self.x_cm_id,
            'Content-Type': 'application/json'
        }

        body = {
            'clientId': self.client_id,
            'clientSecret': self.client_secret,
            'grantType': 'client_credentials'
        }

        try:
            response = requests.post(url, headers=headers, json=body, timeout=5)

            if response.status_code == self.expected_status_code:
                response_data = response.json()
                session_data: SessionData = {
                    'accessToken': response_data['accessToken'],
                    'expiresIn': response_data['expiresIn'],
                    'refreshExpiresIn': response_data['refreshExpiresIn'],
                    'refreshToken': response_data['refreshToken'],
                    'tokenType': response_data['tokenType'],
                    'cachedAt': timezone.now().timestamp(),
                }
                expiry_seconds = session_data['expiresIn']
                cache.set(CACHE_KEY, session_data, timeout=expiry_seconds - 60)
                logger.info("Successfully created and cached new ABDM session.")
                return session_data
            else:
                logger.error(f"Unexpected status code {response.status_code}: {response.text}")
                raise ABDMExternalException(
                    message="Failed to create session with ABDM gateway.",
                    url=url,
                    status_code=response.status_code,
                    response_body=response.text,
                    context="session_creation_error"
                )
        except requests.exceptions.RequestException as e:
            ex = ABDMExternalException(
                message="Request to ABDM gateway failed.",
                url=url,
                status_code=None,
                response_body=str(e),
                context="session_creation_error"
            )
            logger.error(str(ex))
            raise ex

    def refresh_session(self, refresh_token: str) -> SessionData:
        """
        Refreshes the session using the refresh token and caches the new session data.

        Args:
            refresh_token (str): The refresh token from the cached session.

        Returns:
            SessionData: The refreshed session data.

        Raises:
            requests.exceptions.RequestException: If the API call fails.
        """
        url = f"{self.gateway_base_url}{self.session_endpoint}"
        
        headers = {
            'REQUEST-ID': str(uuid.uuid4()),
            'TIMESTAMP': datetime.now().isoformat(),
            'X-CM-ID': self.x_cm_id,
            'Content-Type': 'application/json'
        }
        
        body = {
            'clientId': self.client_id,
            'clientSecret': self.client_secret,
            'grantType': 'refresh_token',
            'refreshToken': refresh_token
        }
        
        try:
            response = requests.post(url, headers=headers, json=body, timeout=5)
            
            if response.status_code == self.expected_status_code:
                response_data = response.json()
                session_data: SessionData = {
                    'accessToken': response_data['accessToken'],
                    'expiresIn': response_data['expiresIn'],
                    'refreshExpiresIn': response_data['refreshExpiresIn'],
                    'refreshToken': response_data['refreshToken'],
                    'tokenType': response_data['tokenType'],
                    'cachedAt': timezone.now().timestamp(),
                }
                expiry_seconds = session_data['expiresIn']
                cache.set(CACHE_KEY, session_data, timeout=expiry_seconds - 60)
                logger.info("Successfully refreshed and cached new ABDM session.")
                return session_data
            else:
                logger.error(f"Unexpected status code {response.status_code}: {response.text}")
                raise ABDMExternalException(
                    message="Failed to refresh session with ABDM gateway.",
                    url=url,
                    status_code=response.status_code,
                    response_body=response.text,
                    context="session_refresh_error"
                )
        except requests.exceptions.RequestException as e:
            ex = ABDMExternalException(
                message="Request to ABDM gateway failed.",
                url=url,
                status_code=None,
                response_body=str(e),
                context="session_refresh_error"
            )
            logger.error(str(ex))
            raise ex

# Singleton instance
abdm_session = ABDMSession() 