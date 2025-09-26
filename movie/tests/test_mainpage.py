from django.test import TestCase
from movie.models import Movie
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus


class Get_test_mainpage(TestCase):
    #Создаем юзера
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )

        #Авторизовываем юзера
        self.client.login(username='testuser', password='testpass123')

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        #проверяет вхождение значения(шаблона) в коллекцию данных
        self.assertIn('movie/index.html', response.template_name)

        #или

        self.assertTemplateUsed(response, 'movie/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')


class Get_test_data_mainpage(TestCase):
    fixtures = ["movie_movie.json", "auth_user.json"]

    #Проверка содержимого страниц

    def test_data_mainpage(self):

        # Авторизуем пользователя (иначе редирект на login)
        self.client.login(username='testuser', password='testpass123')

        # Получаем ожидаемые фильмы (первые 3 из-за paginate_by=3)
        expected_movies = list(Movie.published.all().select_related('cat')[:3])

        # Делаем запрос
        response = self.client.get(reverse('home'))

        # Получаем фактические фильмы из пагинатора
        actual_movies = list(response.context['page_obj'].object_list)

        # Сравниваем списки
        self.assertEqual(actual_movies, expected_movies)


    #Проверка работы пагинации главной страницы
    def test_paginate_mainpage(self):
        self.client.login(username='testuser', password='testpass123')

        path = reverse('home')
        page = 2
        paginate_by = 3
        response = self.client.get(path + f'?page={page}')

        all_movies = Movie.published.all().select_related('cat').order_by('-time_create')
        expected_movies = list(all_movies[(page - 1) * paginate_by : page * paginate_by])
        actual_movies = list(response.context['page_obj'].object_list)

        self.assertEqual(actual_movies, expected_movies)

