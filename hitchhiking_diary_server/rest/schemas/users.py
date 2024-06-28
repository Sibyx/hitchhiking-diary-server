from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserDetailSchema(BaseModel):
    id: UUID
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
