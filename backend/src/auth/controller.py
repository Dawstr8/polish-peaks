from fastapi import APIRouter, HTTPException, Request, Response, status

from src.auth.dependencies import (
    auth_service_dep,
    current_user_dep,
    oauth2_password_request_form_dep,
)
from src.auth.models import Token
from src.config import REFRESH_TOKEN_EXPIRE_DAYS
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


@router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: oauth2_password_request_form_dep,
    auth_service: auth_service_dep,
) -> Token:
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
        access_token, refresh_token = auth_service.login_user_and_create_tokens(
            form_data.username, form_data.password
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    request: Request,
    auth_service: auth_service_dep,
) -> Token:
    """
    Refresh access token.

    Args:
        request: HTTP request
        auth_service: An authentication service

    Returns:
        New access token
    """

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        new_access_token = auth_service.refresh_access_token(refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=new_access_token, token_type="bearer")


@router.post("/logout")
async def logout(
    response: Response,
    auth_service: auth_service_dep,
):
    """
    Logout current user.

    Args:
        response: HTTP response
        auth_service: An authentication service

    Returns:
        Success message
    """
    auth_service.logout_user()

    response.delete_cookie(
        key="refresh_token", httponly=True, secure=True, samesite="lax"
    )

    return {"message": "Successfully logged out"}
