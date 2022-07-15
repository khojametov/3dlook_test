import pytest
from django.urls import reverse


class TestAuthentication:
    @pytest.mark.django_db
    def test_user_registration(self, client):
        url = reverse("register")
        data = {"username": "test", "password": "test", "password2": "test"}
        response = client.post(url, data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_user_registration_with_wrong_password(self, client):
        url = reverse("register")
        data = {"username": "test", "password": "test", "password2": "test2"}
        response = client.post(url, data)
        assert response.status_code == 400

    def test_user_login(self, client, dummy_user):
        url = reverse("login")
        data = {"username": dummy_user.username, "password": dummy_user.dummy_password}
        response = client.post(url, data)
        assert response.status_code == 200
        assert "access" in response.data
