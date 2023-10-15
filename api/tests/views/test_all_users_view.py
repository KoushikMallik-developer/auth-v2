import pytest
from rest_framework.test import APITestCase


@pytest.mark.django_db
class TestAllUsersView(APITestCase):
    def test_get_all_users(self):
        url = "http://localhost/api/v2/all-users"
        response = self.client.get(url, None, format="json")
        assert response
