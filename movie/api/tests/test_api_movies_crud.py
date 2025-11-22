import pytest
from django.contrib.auth.models import User
from rest_framework import status
from movie.models import Movie

@pytest.mark.django_db
def test_movie_list(client, create_movies):
    response = client.get('/api/v1/movies/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 10
    assert len(response.data["results"]) == 3
    assert response.data["results"][0]["title"] == "Test1"

@pytest.mark.django_db
def test_api_movies_pagination(client, create_movies):
    response = client.get('/api/v1/movies/?page_size=3')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 10
    assert response.data['next'] is not None
    assert len(response.data['results']) == 3

@pytest.mark.django_db
def test_api_movie_get(client, create_movies):
    response = client.get('/api/v1/movies/1/')
    assert response.data['title'] == "Test1"
    assert response.status_code == status.HTTP_200_OK
    response_404 = client.get('/api/v1/movies/999/')
    assert response_404.status_code == status.HTTP_404_NOT_FOUND

    data = response.data
    keys = ['id', 'title', 'content', 'time_create', 'time_update']
    for key in keys:
        assert key in data

    assert isinstance(data['id'], int)
    assert isinstance(data['title'], str)
    assert isinstance(data['time_create'], str)  # ISO формат даты

## POST ##
@pytest.mark.django_db
def test_api_movie_post(user, client):
    client.force_authenticate(user=user)
    response = client.post('/api/v1/movies/', data={'title':'TestPostTitle', 'content':'TestPostContent'})
    assert response.status_code == status.HTTP_201_CREATED
    assert Movie.objects.filter(title='TestPostTitle').exists()

    # Проверка присвоения поля user текущему пользователю
    movie = Movie.objects.get(title='TestPostTitle')
    assert movie.user == user

@pytest.mark.django_db
def test_api_movie_post_unauthorized(client):
    response = client.post('/api/v1/movies/', data={
        'title': 'TestPostTitle',
        'content': 'TestPostContent',
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_api_movie_post_creates_slug(user, client):
    client.force_authenticate(user=user)
    response = client.post('/api/v1/movies/', data={
        'title': 'Test_Movie_for_Slug',
        'content': 'Some_content',
    })
    assert response.status_code == status.HTTP_201_CREATED

    # Проверим, что slug сгенерировался правильно
    movie = Movie.objects.get(id=response.data['id'])
    assert movie.slug == 'test_movie_for_slug'

## PUT ##
@pytest.mark.django_db
def test_api_movie_put(user, client, create_movies):
    client.force_authenticate(user=user)
    response = client.put('/api/v1/movies/1/', {"title": "TestPutTitle"})
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_api_movie_put_forbidden(client):
    owner = User.objects.create_user(username="owner", password="pass")
    other = User.objects.create_user(username="other", password="pass")

    movie = Movie.objects.create(
        title="Test Movie",
        content="Test Content",
        user=owner
    )

    client.force_authenticate(user=other)
    response = client.put(f'/api/v1/movies/{movie.id}/', {"title": "Hacked"})
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_api_movie_put_unauthorized(user, client, create_movies):
    response = client.put('/api/v1/movies/1/', {"title": "TestPutTitle"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_api_movie_put_admin(admin_user, client):
    # Создаём владельца (не админа)
    owner = User.objects.create_user(username="owner", password="pass")
    movie = Movie.objects.create(title="Original", content="Content", user=owner)

    # Админ пытается изменить чужой фильм
    client.force_authenticate(user=admin_user)
    response = client.put(f'/api/v1/movies/{movie.id}/', {"title": "TestPutTitle"})
    assert response.status_code == status.HTTP_200_OK

## DELETE ##
@pytest.mark.django_db
def test_api_movie_delete(user, client, create_movies):
    client.force_authenticate(user=user)
    response = client.delete('/api/v1/movies/1/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_api_movie_delete_admin(admin_user, client):
    # Создаём владельца (не админа)
    owner = User.objects.create_user(username="owner", password="pass")
    movie = Movie.objects.create(title="Original", content="Content", user=owner)

    # Админ пытается удалить чужой фильм
    client.force_authenticate(user=admin_user)
    response = client.delete('/api/v1/movies/1/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_api_movie_delete_forbidden(client):
    owner = User.objects.create_user(username="owner", password="pass")
    other = User.objects.create_user(username="other", password="pass")

    movie = Movie.objects.create(
        title="Test Movie",
        content="Test Content",
        user=owner
    )

    client.force_authenticate(user=other)
    response = client.delete('/api/v1/movies/1/')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_api_movie_delete_unauthorized(user, client, create_movies):
    response = client.delete('/api/v1/movies/1/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

## Валидация ##
@pytest.mark.django_db
def test_api_movie_validation(user, client):
    client.force_authenticate(user=user)
    response = client.post('/api/v1/movies/', data={
        # 'title': 'TestPostTitle',
        'content': 'TestPostContent',
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'title' in response.data
    assert 'Обязательное поле.' in response.data['title']

    assert 'title' in response.data
    assert len(response.data['title']) > 0  # есть хотя бы одно сообщение об ошибке

@pytest.mark.django_db
def test_api_movie_max_length(user, client):
    client.force_authenticate(user=user)
    response = client.post('/api/v1/movies/', data={
        'title': "тестирование превышение количества символов указанных в поле title max_length=255, тестирование "
                 "превышение количества символов указанных в поле title max_length=255, тестирование превышение "
                 "количества символов указанных в поле title max_length=255, тестирование превышение количества "
                 "символов указанных в поле title max_length=255 - 338",
        'content': 'TestPostContent',
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_api_movie_correct_slug(user, client):
    client.force_authenticate(user=user)
    response = client.post('/api/v1/movies/', data={
        'title': 'Test_Create_Correct_Slug',
        'content': 'Some_content',
    })
    assert response.status_code == status.HTTP_201_CREATED

    # Проверим, что slug сгенерировался правильно
    movie = Movie.objects.get(id=response.data['id'])
    assert movie.slug == 'test_create_correct_slug'

@pytest.mark.django_db
def test_api_movie_unique_slug(user, client):
    client.force_authenticate(user=user)
    # Первый фильм
    response1 = client.post('/api/v1/movies/', {'title': 'Duplicate Title'})
    assert response1.status_code == 201
    assert response1.data['slug'] == 'duplicate-title'

    # Второй с тем же title → должен получить 'duplicate-title-1'
    response2 = client.post('/api/v1/movies/', {'title': 'Duplicate Title'})
    assert response2.status_code == 201
    assert response2.data['slug'] == 'duplicate-title-1'

## Авторизация ##
@pytest.mark.django_db
def test_api_movie_login(user, client):
    response = client.post('/api/v1/token/', {"username": "test_user", "password": "password123"})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_api_movie_wrong_password(user, client):
    response = client.post('/api/v1/token/', {"username": "test_user", "password": "password999"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_api_movie_refresh_token(user, client):
    response = client.post('/api/v1/token/', {"username": "test_user", "password": "password123"})
    assert response.status_code == status.HTTP_200_OK
    old_access = response.data['access']
    refresh_token = response.data['refresh']
    response_refresh = client.post('/api/v1/token/refresh/', {"refresh": refresh_token})
    assert response_refresh.status_code == status.HTTP_200_OK
    assert 'access' in response_refresh.data
    new_access = response_refresh.data['access']
    assert new_access != old_access

@pytest.mark.django_db
def test_api_movie_verify(user, client):
    response = client.post('/api/v1/token/', {"username": "test_user", "password": "password123"})
    assert response.status_code == status.HTTP_200_OK
    access_token = response.data['access']
    response_verify = client.post('/api/v1/token/verify/', {"token": access_token})
    assert response_verify.status_code == status.HTTP_200_OK