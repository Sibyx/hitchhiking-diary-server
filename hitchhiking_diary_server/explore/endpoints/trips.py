from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse

from hitchhiking_diary_server.core import templates, settings
from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import Trip, User, Photo

router = APIRouter()


@router.get("/trips/{trip_id}", response_class=HTMLResponse)
async def explore_trip_detail(request: Request, trip_id: UUID, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip does not exist!")

    return templates.TemplateResponse(
        request=request,
        name="explore/trip.html",
        context={
            "trip": trip
        }
    )


@router.get("/photos/{photo_id}")
async def explore_download_photo(photo_id: UUID, db: Session = Depends(get_db)):
    # FIXME: security tokens using redis
    photo = db.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo does not exist!")

    return FileResponse(settings.DATA_DIR / photo.path, media_type=photo.mime)
