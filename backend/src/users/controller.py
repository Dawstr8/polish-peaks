from fastapi import APIRouter, HTTPException, status

from src.tokens.models import AccessToken
from src.users.dependencies import (
    current_user_dep,
    oauth2_password_request_form_dep,
    users_service_dep,
)
from src.users.models import UserCreate, UserRead

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    users_service: users_service_dep,
):
    """
    Register a new user.

    Args:
        user_create: Data for creating a new user
        users_service: Users service

    Returns:
        The created User object
    """
    try:
        return await users_service.register_user(user_create)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/me", response_model=UserRead)
async def read_users_me(
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


@router.post("/token", response_model=AccessToken)
async def login_for_access_token(
    form_data: oauth2_password_request_form_dep,
    users_service: users_service_dep,
) -> AccessToken:
    """
    Login for access token.

    Args:
        form_data: OAuth2 form data
        users_service: Users service

    Returns:
        Access token

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        token = users_service.login_user_and_create_token(
            form_data.username, form_data.password
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
