from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus
from movie.models import Movie


class MovieViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            slug='test-movie',
            content='Test content',
            user=self.user
        )

    def test_movie_detail(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/post/{self.movie.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertContains(response, 'Test content')