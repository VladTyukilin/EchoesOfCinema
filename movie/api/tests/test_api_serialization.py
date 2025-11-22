import pytest
from movie.api.tests.conftest import create_movies

@pytest.mark.django_db
def test_api_movies_serialization(user, client, create_movies):
    client.force_authenticate(user=user)
    response_get = client.get('/api/v1/movies/')
    response_post = client.post('/api/v1/movies/', data={'title':'TestPostTitle', 'content':'TestPostContent'})
    response_put = client.put('/api/v1/movies/1/', {"title": "TestPutTitle"})
    response_delete = client.delete('/api/v1/movies/1/')
    assert response_get.status_code == 200
    assert response_post.status_code == 201
    assert response_put.status_code == 200
    assert response_delete.status_code == 204


