from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAdminUser  # Removed admin-only access

from .services import abdm_session
from .exceptions import ABDMExternalException

class GetABDMSessionView(APIView):
    """
    API View to get the current ABDM session (with proactive refresh).
    """
    # permission_classes = [IsAdminUser]  # Removed admin-only access

    def get(self, request, *args, **kwargs):
        """
        Retrieve the current ABDM session, returning session data if available.
        
        Returns:
            Response: HTTP 200 with session data if found, or HTTP 404 with error details if no session exists.
        """
        try:
            session_data = abdm_session.get_session()
            return Response(session_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "No session found", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

class CreateABDMSessionView(APIView):
    """
    API View to create a new ABDM session.
    """
    # permission_classes = [IsAdminUser]  # Removed admin-only access

    def post(self, request, *args, **kwargs):
        """
        Create a new ABDM session and return its data.
        
        On success, returns the created session data with HTTP 201 status. If an ABDMExternalException occurs, returns detailed error information and the appropriate status code. For any other exception, returns a generic error message with HTTP 500 status.
        """
        try:
            session_data = abdm_session.create_session()
            return Response(session_data, status=status.HTTP_201_CREATED)
        except ABDMExternalException as e:
            return Response({
                "error": str(e),
                "context": e.context,
                "url": e.url,
                "status_code": e.status_code,
                "response_body": e.response_body,
            }, status=e.status_code if e.status_code else 502)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RefreshABDMSessionView(APIView):
    """
    API View to refresh the ABDM session using the refresh token.
    Throws an exception if the cache is empty.
    """
    # permission_classes = [IsAdminUser]  # Removed admin-only access

    def post(self, request, *args, **kwargs):
        """
        Refreshes the ABDM session using the current session's refresh token.
        
        Returns:
            Response: Refreshed session data with HTTP 200 OK on success, or an error message with HTTP 404 Not Found if the refresh fails.
        """
        try:
            session = abdm_session.get_session()
            refresh_token = session['refreshToken']
            session_data = abdm_session.refresh_session(refresh_token)
            return Response(session_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Cannot refresh session", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND
            ) 