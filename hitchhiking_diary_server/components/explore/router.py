from fastapi import APIRouter

from .endpoints import trips

router = APIRouter()
router.include_router(trips.router)
