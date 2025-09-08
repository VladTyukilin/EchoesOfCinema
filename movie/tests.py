from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Movie, Category


class MovieModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')

    def test_create_movie(self):
        movie = Movie.objects.create(
            title='Test Movie',
            slug='test-movie',
            content='Test content',
            cat=self.category,
            user=self.user
        )
        self.assertEqual(str(movie), 'Test Movie')
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(movie.cat.name, 'Test Category')


class MovieViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.movie = Movie.objects.create(
            title='Test Movie',
            slug='test-movie',
            content='Test content',
            cat=self.category,
            user=self.user
        )

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_movie_detail(self):
        response = self.client.get(f'/post/{self.movie.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertContains(response, 'Test content')