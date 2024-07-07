from fastapi import APIRouter, Depends

from hitchhiking_diary_server.models import User
from hitchhiking_diary_server.components.rest.auth import get_current_user
from hitchhiking_diary_server.components.rest.schemas.users import UserDetailSchema

router = APIRouter()


@router.get("/users/me", response_model=UserDetailSchema)
def read_users_me(user: User = Depends(get_current_user)):
    return user
