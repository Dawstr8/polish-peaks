from fastapi import APIRouter, HTTPException, status

from src.auth.dependencies import (
    auth_service_dep,
    current_user_dep,
    oauth2_password_request_form_dep,
)
from src.tokens.models import AccessToken
from src.users.models import UserCreate, UserRead

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    auth_service: auth_service_dep,
):
    """
    Register a new user.

    Args:
        user_create: Data for creating a new user
        auth_service: An authentication service

    Returns:
        The created User object
    """
    try:
        return await auth_service.register_user(user_create)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/me", response_model=UserRead)
async def read_me(
    current_user: current_user_dep,
):
    """
    Get current user info.

    Args:
        current_user: Current active user

    Returns:
        Current user
    """
    return current_user


@router.post("/login", response_model=AccessToken)
async def login_for_access_token(
    form_data: oauth2_password_request_form_dep,
    auth_service: auth_service_dep,
) -> AccessToken:
    """
    Login for access token.

    Args:
        form_data: OAuth2 form data
        auth_service: An authentication service

    Returns:
        Access token

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        token = auth_service.login_user_and_create_token(
            form_data.username, form_data.password
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
