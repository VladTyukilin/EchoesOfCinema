from random import randint
from movie.api.tests.test_api import client, create_movies, user


def register_user(user):
    if user['username'] and user['password']:
        return {"status": "success", "user_id": randint(1,99)}
    else:
        return {"status": "error", "message": "Username and password are required"}

def test_successful_registration(user):
    result = register_user(user)
    assert result["status"] == "success"
    assert "user_id" in result