from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from hitchhiking_diary_server.core import settings
from hitchhiking_diary_server.components.rest.router import router as rest_router
from hitchhiking_diary_server.components.explore.router import router as explore_router
from hitchhiking_diary_server.components.images.router import router as images_router

app = FastAPI(title=settings.NAME, version=settings.VERSION, description=settings.DESCRIPTION)

app.mount("/static", StaticFiles(directory=settings.BASE_DIR / "static"), name="static")

# REST
app.include_router(rest_router, prefix="/api/v1")

# Explore
app.include_router(explore_router, tags=["Explore"])

# Images
app.include_router(images_router, prefix="/images/v1", tags=["Images"])
