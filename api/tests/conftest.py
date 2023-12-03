import pytest

from api.models.user import ECOMUser


@pytest.fixture
def user_list():
    return [
        {
            "id": "a0309afd-2f4a-4726-9903-fb07e3d7500e",
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
            "id": "8a3a52ad-bb84-425c-bda7-884effd28374",
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
