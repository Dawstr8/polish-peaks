from uuid import UUID

from fastapi.testclient import TestClient

BASE_URL = "/api/auth"
REGISTER_ENDPOINT = f"{BASE_URL}/register"
ME_ENDPOINT = f"{BASE_URL}/me"
LOGIN_ENDPOINT = f"{BASE_URL}/login"
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


def test_read_me_success(client_with_db: TestClient, logged_in_user):
    """Test getting current user info with valid session"""
    response = client_with_db.get(ME_ENDPOINT)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == logged_in_user["email"]
    assert "created_at" in data


def test_read_me_no_session(client_with_db: TestClient):
    """Test accessing me endpoint without session cookie"""
    response = client_with_db.get(ME_ENDPOINT)

    assert response.status_code == 401
    data = response.json()
    assert "Not authenticated" in data["detail"]


def test_read_me_invalid_session(client_with_db: TestClient):
    """Test accessing me endpoint with invalid session"""
    client_with_db.cookies.set(
        "session_id", str(UUID("12345678-1234-5678-1234-567812345678"))
    )

    response = client_with_db.get(ME_ENDPOINT)

    assert response.status_code == 401
    data = response.json()
    assert "Invalid or expired session" in data["detail"]


def test_login_with_session_success(client_with_db: TestClient, registered_user):
    """Test successful login and session creation"""

    response = client_with_db.post(
        LOGIN_ENDPOINT,
        data={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

    assert "session_id" in response.cookies
    assert response.cookies.get("session_id") is not None


def test_login_with_session_invalid_credentials(client_with_db: TestClient):
    """Test login with invalid credentials"""
    response = client_with_db.post(
        LOGIN_ENDPOINT,
        data={"email": "nonexistent@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "Incorrect email or password" in data["detail"]


def test_logout_success(client_with_db: TestClient, logged_in_user):
    """Test successful logout and session invalidation"""
    before_logout_me_response = client_with_db.get(ME_ENDPOINT)

    response = client_with_db.post(LOGOUT_ENDPOINT)

    after_logout_me_response = client_with_db.get(ME_ENDPOINT)
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}
    assert "session_id" not in response.cookies
    assert before_logout_me_response.status_code == 200
    assert after_logout_me_response.status_code == 401
