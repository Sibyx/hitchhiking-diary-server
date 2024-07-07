from datetime import datetime

from pydantic import BaseModel, Field


class StatusSchema(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
