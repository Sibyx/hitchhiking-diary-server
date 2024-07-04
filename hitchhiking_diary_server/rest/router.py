from fastapi import APIRouter

from .endpoints import tokens
from .endpoints import users
from .endpoints import photos
from .endpoints import sync
from .endpoints import status

router = APIRouter()
router.include_router(tokens.router, tags=["Tokens"])
router.include_router(users.router, tags=["Users"])
router.include_router(photos.router, tags=["Photos"])
router.include_router(sync.router, tags=["Synchronization"])
router.include_router(status.router, tags=["Status"])
