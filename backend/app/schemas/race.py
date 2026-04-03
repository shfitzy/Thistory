from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class RaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) else v


class RaceCreate(RaceBase):
    pass


class RaceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) and v else v


class RaceInDB(RaceBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Race(RaceInDB):
    pass
