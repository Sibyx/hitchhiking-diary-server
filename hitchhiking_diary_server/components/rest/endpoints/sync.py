from fastapi import APIRouter, Depends
from geoalchemy2 import WKTElement
from sqlalchemy import or_
from sqlalchemy.orm import Session

from hitchhiking_diary_server.db.session import get_db
from hitchhiking_diary_server.models import User, Trip, TripRecord, Photo
from hitchhiking_diary_server.components.rest.auth import get_current_user
from hitchhiking_diary_server.components.rest.schemas.sync import SyncRequestSchema, SyncResponseSchema

router = APIRouter()


@router.post("/sync", response_model=SyncResponseSchema)
async def sync(
    form: SyncRequestSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Trips
    for item in form.trips:
        trip = db.query(Trip).filter(Trip.id == item.id).first()

        if trip:
            if trip.user_id != user.id:
                continue

            if item.updated_at > trip.updated_at:
                trip.title = item.title
                trip.content = item.content
                trip.status = item.status
                trip.deleted_at = item.deleted_at
                db.commit()
        else:
            trip = Trip(
                id=item.id,
                title=item.title,
                user_id=user.id,
                status=item.status,
                content=item.content,
                deleted_at=item.deleted_at,
            )
            db.add(trip)
            db.commit()

    # TripRecord
    for item in form.records:
        record = db.query(TripRecord).filter(TripRecord.id == item.id).first()

        location = WKTElement(f"POINT({item.latitude} {item.longitude})", srid=4326)

        if record:
            if record.trip.user_id != user.id:
                continue

            if item.updated_at > record.updated_at:
                record.type = item.type
                record.content = item.content
                record.location = location
                record.happened_at = item.happened_at
                record.deleted_at = item.deleted_at
                db.commit()
        else:
            record = TripRecord(
                id=item.id,
                trip_id=item.trip_id,
                type=item.type,
                location=location,
                content=item.content,
                happened_at=item.happened_at,
                deleted_at=item.deleted_at,
            )
            db.add(record)
            db.commit()

    # Photos
    for item in form.photos:
        photo = db.query(Photo).filter(Photo.id == item.id).first()

        if photo:
            if photo.record.trip.user_id != user.id:
                continue

            if item.updated_at > photo.updated_at:
                photo.deleted_at = item.deleted_at
                db.commit()
        else:
            photo = Photo(id=item.id, record_id=item.record_id, deleted_at=item.deleted_at)
            db.add(photo)
            db.commit()

    trips = db.query(Trip).filter(Trip.user_id == user.id)
    records = db.query(TripRecord).join(Trip).filter(Trip.user_id == user.id)
    photos = db.query(Photo).join(TripRecord).join(Trip).filter(Trip.user_id == user.id)

    if form.last_sync_at:
        trips = trips.filter(Trip.updated_at >= form.last_sync_at)
        records = records.filter(TripRecord.updated_at >= form.last_sync_at)
        photos = photos.filter(or_(Photo.created_at >= form.last_sync_at, Photo.deleted_at >= form.last_sync_at))

    return SyncResponseSchema(trips=trips.all(), records=records.all(), photos=photos.all())
