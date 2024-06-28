from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TripRecordSyncSchema(BaseModel):
    id: UUID
    trip_id: UUID
    type: str
    content: Optional[str] = None
    latitude: float
    longitude: float
    happened_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class TripRecordDetailSchema(BaseModel):
    id: UUID
    trip_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
