from fastapi import APIRouter

from .endpoints import opengraph

router = APIRouter()
router.include_router(opengraph.router)
