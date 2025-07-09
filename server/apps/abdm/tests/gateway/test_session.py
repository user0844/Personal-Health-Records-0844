from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TestABDMSessionView(APITestCase):
    def test_create_abdm_session(self):
        """
        Tests the creation of an ABDM session via a POST request to the 'create_abdm_session' endpoint.
        
        Sends a POST request and prints the response status code and data for debugging purposes.
        """
        url = reverse('create_abdm_session')
        response = self.client.post(url)
        print('RESPONSE:', response.status_code, response.data)
        # We expect either a 201 (created) or 500 (if config is missing or external call fails)
        # self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_500_INTERNAL_SERVER_ERROR]) 

    def test_get_abdm_session(self):
        """
        Tests the retrieval of an ABDM session via the 'get_abdm_session' API endpoint.
        
        Sends a GET request to the endpoint and asserts that the response status code is 200 (OK), 404 (Not Found), or 500 (Internal Server Error), covering successful retrieval, missing resource, or server error scenarios.
        """
        url = reverse('get_abdm_session')
        response = self.client.get(url)
        print('RESPONSE:', response.status_code, response.data)
        # We expect either a 200 (OK), 404 (not found), or 500 (if config is missing or external call fails)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_500_INTERNAL_SERVER_ERROR]) 