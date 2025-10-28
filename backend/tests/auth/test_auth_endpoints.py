from fastapi.testclient import TestClient

BASE_URL = "/api/auth"
REGISTER_ENDPOINT = f"{BASE_URL}/register"
ME_ENDPOINT = f"{BASE_URL}/me"
LOGIN_ENDPOINT = f"{BASE_URL}/login"
REFRESH_ENDPOINT = f"{BASE_URL}/refresh"
LOGOUT_ENDPOINT = f"{BASE_URL}/logout"


def test_register_user_success(client_with_db: TestClient):
    """Test registering a new user successfully"""
    response = client_with_db.post(
        REGISTER_ENDPOINT, json={"email": "user1@example.com", "password": "pass123"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user1@example.com"
    assert "created_at" in data


def test_register_user_duplicate_email(client_with_db: TestClient):
    """Test registering a user with a duplicate email"""
    client_with_db.post(
        REGISTER_ENDPOINT, json={"email": "user2@example.com", "password": "pass123"}
    )

    response = client_with_db.post(
        REGISTER_ENDPOINT, json={"email": "user2@example.com", "password": "pass456"}
    )

    assert response.status_code == 400
    assert "already in use" in response.json()["detail"]


def test_register_user_invalid_email(client_with_db: TestClient):
    """Test registering a user with invalid email format"""
    response = client_with_db.post(
        REGISTER_ENDPOINT, json={"email": "invalid-email", "password": "pass123"}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("email" in str(error) for error in data["detail"])


def test_read_users_me_success(client_with_db: TestClient, logged_in_user):
    """Test getting current user info with valid token"""
    token = logged_in_user["token"]

    response = client_with_db.get(
        ME_ENDPOINT, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == logged_in_user["email"]
    assert "created_at" in data


def test_read_users_me_no_token(client_with_db: TestClient):
    """Test accessing me endpoint without token"""
    response = client_with_db.get(ME_ENDPOINT)

    assert response.status_code == 401
    data = response.json()
    assert "Not authenticated" in data["detail"]


def test_read_users_me_invalid_token(client_with_db: TestClient):
    """Test accessing me endpoint with invalid token"""
    response = client_with_db.get(
        ME_ENDPOINT, headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    data = response.json()
    assert "Could not validate credentials" in data["detail"]


def test_login_for_access_token_success(client_with_db: TestClient, registered_user):
    """Test successful login and token retrieval"""

    response = client_with_db.post(
        LOGIN_ENDPOINT,
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


def test_login_for_access_token_invalid_credentials(client_with_db: TestClient):
    """Test login with invalid credentials"""
    response = client_with_db.post(
        LOGIN_ENDPOINT,
        data={"username": "nonexistent@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "Incorrect email or password" in data["detail"]


def test_refresh_access_token_success(client_with_db: TestClient, logged_in_user):
    """Test refreshing access token with valid refresh token"""
    refresh_response = client_with_db.post(REFRESH_ENDPOINT)

    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


def test_refresh_access_token_no_refresh_token(client_with_db: TestClient):
    """Test refreshing access token without refresh token"""
    response = client_with_db.post(REFRESH_ENDPOINT)

    assert response.status_code == 401
    data = response.json()
    assert "Refresh token missing" in data["detail"]


def test_refresh_access_token_invalid_refresh_token(client_with_db: TestClient):
    """Test refreshing access token with invalid refresh token"""
    client_with_db.cookies.set("refresh_token", "invalid_refresh_token")

    response = client_with_db.post(REFRESH_ENDPOINT)

    assert response.status_code == 401
    data = response.json()
    assert "Invalid refresh token" in data["detail"]


def test_logout_success(client_with_db: TestClient, logged_in_user):
    """Test successful user logout"""
    before_refresh_response = client_with_db.post(REFRESH_ENDPOINT)

    response = client_with_db.post(LOGOUT_ENDPOINT)

    after_refresh_response = client_with_db.post(REFRESH_ENDPOINT)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully logged out"

    assert before_refresh_response.status_code == 200
    assert after_refresh_response.status_code == 401


def test_logout_no_token(client_with_db: TestClient):
    """Test logout without being logged in"""
    response = client_with_db.post(LOGOUT_ENDPOINT)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully logged out"
