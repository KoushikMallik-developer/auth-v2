import pytest

from api.models.user import ECOMUser


@pytest.fixture
def user_list():
    return [
        {
            "id": "koushikmallik001@gmail.com",
            "username": "koushikmallik",
            "email": "koushikmallik001@gmail.com",
            "fname": "Koushik",
            "lname": "Google",
            "dob": None,
            "phone": None,
            "image": "/images/users/defaultUserImage.png",
            "is_active": False,
            "account_type": "Regular",
        },
        {
            "id": "animeshece1998@gmail.com",
            "username": "koushikmallik",
            "email": "animeshece1998@gmail.com",
            "fname": "Koushik",
            "lname": "Google",
            "dob": None,
            "phone": None,
            "image": "/images/users/defaultUserImage.png",
            "is_active": False,
            "account_type": "Regular",
        },
    ]


@pytest.fixture
def create_test_user(user_list):
    for user in user_list:
        ECOMUser(**user).save()
