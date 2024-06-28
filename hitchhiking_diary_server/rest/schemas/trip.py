from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TripSyncSchema(BaseModel):
    id: UUID
    title: str
    content: Optional[str] = None
    status: str
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class TripDetailSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    content: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
