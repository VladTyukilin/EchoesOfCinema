from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from movie.models import Movie


class GetPagesTestCase(TestCase):
    fixtures = ["movie_movie.json", "auth_user.json"]

    #Создаем юзера
    def setUp(self):

        #Авторизовываем юзера
        self.client.login(username='testuser', password='testpass123')

    #проверка содержимого страницы отображения поста
    def test_content_post(self):
        expected_post = Movie.objects.get(pk=1)
        path = reverse('post', args=[expected_post.slug])
        response = self.client.get(path)
        self.assertEqual(expected_post.content, response.context['movie'].content)

    #проверка перенаправления со страницы: http://127.0.0.1:8000/add_movie/
    def test_redirect_addpage(self):
        #Деавторизовываем юзера
        self.client.logout()

        path = reverse('add_movie')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)