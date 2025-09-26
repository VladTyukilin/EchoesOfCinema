from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus
from movie.models import Movie


class MovieModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_movie(self):
        movie = Movie.objects.create(
            title='Test Movie',
            slug='test-movie',
            content='Test content',
            user=self.user
        )
        self.assertEqual(str(movie), 'Test Movie')
        self.assertEqual(Movie.objects.count(), 1)