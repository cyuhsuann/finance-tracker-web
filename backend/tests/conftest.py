import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="c.yuhsuann", email="c.yuhsuann@gmail.com", password="c.yuhsuann"
    )


@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(
        username="another_user", email="testing@gmail.com", password="testing"
    )
