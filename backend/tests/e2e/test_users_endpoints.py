from fastapi.testclient import TestClient


def test_register_user_success(client_with_db: TestClient):
    """Test registering a new user successfully"""
    response = client_with_db.post(
        "/users/", json={"email": "user1@example.com", "password": "pass123"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert "created_at" in data


def test_register_user_duplicate_email(client_with_db: TestClient):
    """Test registering a user with a duplicate email"""
    client_with_db.post(
        "/users/", json={"email": "user2@example.com", "password": "pass123"}
    )

    response = client_with_db.post(
        "/users/", json={"email": "user2@example.com", "password": "pass456"}
    )

    assert response.status_code == 400
    assert "already in use" in response.json()["detail"]


def test_register_user_invalid_email(client_with_db: TestClient):
    """Test registering a user with invalid email format"""
    response = client_with_db.post(
        "/users/", json={"email": "invalid-email", "password": "pass123"}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("email" in str(error) for error in data["detail"])
