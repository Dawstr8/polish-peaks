from fastapi.testclient import TestClient


def test_register_user_success(client_with_db: TestClient):
    """Test registering a new user successfully"""
    response = client_with_db.post(
        "/api/users/", json={"email": "user1@example.com", "password": "pass123"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert "created_at" in data


def test_register_user_duplicate_email(client_with_db: TestClient):
    """Test registering a user with a duplicate email"""
    client_with_db.post(
        "/api/users/", json={"email": "user2@example.com", "password": "pass123"}
    )

    response = client_with_db.post(
        "/api/users/", json={"email": "user2@example.com", "password": "pass456"}
    )

    assert response.status_code == 400
    assert "already in use" in response.json()["detail"]


def test_register_user_invalid_email(client_with_db: TestClient):
    """Test registering a user with invalid email format"""
    response = client_with_db.post(
        "/api/users/", json={"email": "invalid-email", "password": "pass123"}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("email" in str(error) for error in data["detail"])


def test_login_for_access_token_success(client_with_db: TestClient):
    """Test successful login and token retrieval"""
    client_with_db.post(
        "/api/users/", json={"email": "login_test@example.com", "password": "pass123"}
    )

    response = client_with_db.post(
        "/api/users/token",
        data={"username": "login_test@example.com", "password": "pass123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


def test_login_for_access_token_invalid_credentials(client_with_db: TestClient):
    """Test login with invalid credentials"""
    response = client_with_db.post(
        "/api/users/token",
        data={"username": "nonexistent@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "Incorrect email or password" in data["detail"]


def test_read_users_me_success(client_with_db: TestClient):
    """Test getting current user info with valid token"""

    client_with_db.post(
        "/api/users/", json={"email": "me_test@example.com", "password": "pass123"}
    )

    login_response = client_with_db.post(
        "/api/users/token",
        data={"username": "me_test@example.com", "password": "pass123"},
    )
    token = login_response.json()["access_token"]

    response = client_with_db.get(
        "/api/users/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me_test@example.com"
    assert "created_at" in data


def test_read_users_me_no_token(client_with_db: TestClient):
    """Test accessing me endpoint without token"""
    response = client_with_db.get("/api/users/me")

    assert response.status_code == 401
    data = response.json()
    assert "Not authenticated" in data["detail"]


def test_read_users_me_invalid_token(client_with_db: TestClient):
    """Test accessing me endpoint with invalid token"""
    response = client_with_db.get(
        "/api/users/me", headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    data = response.json()
    assert "Could not validate credentials" in data["detail"]
