from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    event_date: str = Field(..., min_length=1)
    event_date_end: Optional[str] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) else v


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    event_date: Optional[str] = Field(None, min_length=1)
    event_date_end: Optional[str] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) and v else v


class EventInDB(EventBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Event(EventInDB):
    pass
