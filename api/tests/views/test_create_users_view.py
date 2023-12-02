import pytest
from rest_framework.test import APITestCase


@pytest.mark.django_db
class TestCreateUsersView(APITestCase):
    def test_create_user(self):
        data = {
            "username": "koushikmallik",
            "email": "abcdef@googls.com",
            "fname": "Koushik",
            "lname": "Google",
            "password1": "1234567",
            "password2": "1234567",
        }
        url = "http://localhost/api/v2/create-users"
        response = self.client.post(url, data, format="json")
        assert response
        response = response.json()
        if response.get("error"):
            assert isinstance(response.get("errorMessage"), str)
        else:
            assert response.get("token")
            assert response.get("token").get("refresh")
            assert response.get("token").get("access")
