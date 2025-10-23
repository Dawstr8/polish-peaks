import pytest


@pytest.fixture
def registered_user(client_with_db):
    """Creates and returns a registered user for testing"""
    email = "test@example.com"
    password = "pass123"

    client_with_db.post(
        "/api/auth/register", json={"email": email, "password": password}
    )

    return {"email": email, "password": password}


@pytest.fixture
def logged_in_user(client_with_db, registered_user):
    """Creates and returns a logged-in user for testing"""
    email = registered_user["email"]
    password = registered_user["password"]

    login_response = client_with_db.post(
        "/api/auth/login",
        data={"username": email, "password": password},
    )

    token = login_response.json()["access_token"]

    return {
        "email": email,
        "password": password,
        "token": token,
    }
