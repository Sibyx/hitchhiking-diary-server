from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from hitchhiking_diary_server.components.rest.schemas.photos import PhotoSyncSchema, PhotoDetailSchema
from hitchhiking_diary_server.components.rest.schemas.trip import TripDetailSchema, TripSyncSchema
from hitchhiking_diary_server.components.rest.schemas.trip_record import TripRecordDetailSchema, TripRecordSyncSchema


class SyncRequestSchema(BaseModel):
    trips: List[TripSyncSchema]
    records: List[TripRecordSyncSchema]
    photos: List[PhotoSyncSchema]
    last_sync_at: Optional[datetime] = None


class SyncResponseSchema(BaseModel):
    trips: List[TripDetailSchema]
    records: List[TripRecordDetailSchema]
    photos: List[PhotoDetailSchema]
