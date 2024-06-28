from datetime import datetime

from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from hitchhiking_diary_server.core.conf import settings
from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import User
from hitchhiking_diary_server.rest.schemas.token import TokenFormSchema, TokenDetailSchema

router = APIRouter()


@router.post("/tokens", response_model=TokenDetailSchema)
async def created_token(form: TokenFormSchema, db: Session = Depends(get_db)):
    hasher = PasswordHasher()

    user = db.query(User).filter(User.username == form.username).first()

    if not user or not hasher.verify(user.password, form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = {"sub": user.username, "exp": datetime.now() + settings.ACCESS_TOKEN_EXPIRES}

    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM)

    return TokenDetailSchema(access_token=access_token)
