import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def dummy_user(db):
    data = {"username": "user1", "password": "user1"}
    user = get_user_model().objects.create_user(**data)
    user.dummy_password = data["password"]
    return user


@pytest.fixture
def token(db, dummy_user):
    return str(RefreshToken.for_user(dummy_user).access_token)
