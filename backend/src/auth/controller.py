from uuid import UUID

from fastapi import APIRouter, Cookie, Form, HTTPException, Response, status
from pydantic import EmailStr

from src.auth.dependencies import auth_service_dep, current_user_dep
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


@router.post("/login")
async def login_with_session(
    response: Response,
    auth_service: auth_service_dep,
    email: EmailStr = Form(...),
    password: str = Form(...),
):
    """
    Login with session cookie.

    Args:
        response: FastAPI response object
        auth_service: An authentication service
        email: User's email
        password: User's plain text password

    Returns:
        Success message

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        session_id = auth_service.login_user(email, password)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    response.set_cookie(
        key="session_id",
        value=str(session_id),
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
    )

    return {"message": "Login successful"}


@router.post("/logout")
async def logout_session(
    response: Response,
    auth_service: auth_service_dep,
    session_id: UUID = Cookie(None),
):
    """
    Logout user (session authentication).

    Args:
        response: FastAPI response object
        auth_service: An authentication service
        session_id: Session ID from cookie

    Returns:
        Success message
    """
    if session_id:
        auth_service.logout_user(session_id=session_id)

    response.delete_cookie(key="session_id")
    return {"message": "Logout successful"}
