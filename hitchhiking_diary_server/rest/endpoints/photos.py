import hashlib
import os
import shutil

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from starlette import status
from starlette.responses import FileResponse, Response

from hitchhiking_diary_server.core.conf import settings
from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import Photo, User
from hitchhiking_diary_server.rest.auth import get_current_user
from hitchhiking_diary_server.rest.schemas.photos import PhotoDetailSchema

router = APIRouter()


@router.post("/photos/{photo_id}", response_model=PhotoDetailSchema)
async def upload_photo(
    photo_id: UUID,
    file: UploadFile,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo does not exist!")

    if photo.path:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Photos are immutable!!")

    if photo.record.trip.user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions!")

    trip_upload_location = settings.DATA_DIR / "trips" / photo.record.trip_id
    os.makedirs(trip_upload_location, exist_ok=True)
    file_location = trip_upload_location / file.filename

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    buf_size = 65536
    checksum = hashlib.sha256()

    with open(file_location, "rb") as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            checksum.update(data)

    photo.path = file_location
    photo.mime = file.content_type
    photo.checksum = checksum.hexdigest()

    db.commit()
    db.refresh(photo)

    return photo


@router.get("/photos/{photo_id}")
async def download_photo(
    photo_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo does not exist!")

    if photo.record.trip.user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions!")

    return FileResponse(photo.path, media_type=photo.mime)


@router.delete("/photos/{photo_id}")
async def delete_photo(
    photo_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo does not exist!")

    if photo.record.trip.user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions!")

    db.delete(photo)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
