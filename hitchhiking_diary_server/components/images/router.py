from fastapi import APIRouter

from .endpoints import opengraph
from .endpoints import story

router = APIRouter()
router.include_router(opengraph.router)
router.include_router(story.router)
