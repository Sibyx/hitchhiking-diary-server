from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PhotoSyncSchema(BaseModel):
    id: UUID
    record_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class PhotoDetailSchema(BaseModel):
    id: UUID
    record_id: UUID
    mime: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
