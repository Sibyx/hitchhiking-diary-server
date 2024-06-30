from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from hitchhiking_diary_server.models import TripStatus


class TripSyncSchema(BaseModel):
    id: UUID
    title: str
    content: Optional[str] = None
    status: TripStatus
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class TripDetailSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    content: Optional[str] = None
    status: TripStatus
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
