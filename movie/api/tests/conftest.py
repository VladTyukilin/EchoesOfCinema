import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from movie.models import Movie


@pytest.fixture
def user():
    return User.objects.create_user(username="test_user", password="password123", id=1)

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username="admin", password="admin123")

@pytest.fixture
def authenticated_client(user, client):
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def unauthenticated_client(client):
    return client

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def create_movies(user):
    for i in range(1, 11):
        Movie.objects.create(title=f"Test{i}", content=f"TestContent{i}", user=user)
