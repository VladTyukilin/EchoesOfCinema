import pytest
from movie.models import Movie
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_movie_permissions(client, user, admin_user):
    movie = Movie.objects.create(title="Test", user=user)

    # Анонимный пользователь — только чтение
    response = client.get(f'/api/v1/movies/{movie.id}/')
    assert response.status_code == 200

    response = client.put(f'/api/v1/movies/{movie.id}/', {'title': 'New'})
    assert response.status_code == 401  # или 403

    # Владелец — может редактировать
    client.force_authenticate(user=user)
    response = client.put(f'/api/v1/movies/{movie.id}/', {'title': 'New Title'})
    assert response.status_code == 200

    # Другой пользователь — не может
    other_user = User.objects.create_user(username="other", password="123")
    client.force_authenticate(user=other_user)
    response = client.put(f'/api/v1/movies/{movie.id}/', {'title': 'Hacked'})
    assert response.status_code == 403

    # Админ — может
    client.force_authenticate(user=admin_user)
    response = client.put(f'/api/v1/movies/{movie.id}/', {'title': 'Admin Edit'})
    assert response.status_code == 200