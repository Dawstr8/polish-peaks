from fastapi import APIRouter, HTTPException, status

from src.users.dependencies import users_service_dep
from src.users.models import UserCreate, UserRead

router = APIRouter(
    prefix="/users",
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
