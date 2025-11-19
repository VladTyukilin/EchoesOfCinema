import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from movie.models import Movie

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username = "test_user", password = "password123")

@pytest.fixture
def create_movies():
    Movie.objects.create(title="Test1", content="TestContent1")
    Movie.objects.create(title="Test2", content="TestContent2")

@pytest.mark.django_db
def test_movie_list_is_accessible(client, create_movies):
    response  = client.get('/api/v1/movies/')
    assert response .status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['title'] == 'Test1'
    assert response.data['results'][1]['title'] == 'Test2'