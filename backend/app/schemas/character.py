from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

VALID_STATUSES = {'living', 'deceased', 'unknown'}


class CharacterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    status: str = Field(default='unknown')
    age: Optional[int] = None
    race_id: Optional[int] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in VALID_STATUSES:
            raise ValueError("Status must be 'living', 'deceased', or 'unknown'")
        return v

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError("Age must be a positive integer")
        return v


class CharacterCreate(CharacterBase):
    pass


class CharacterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[str] = None
    age: Optional[int] = None
    race_id: Optional[int] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) and v else v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in VALID_STATUSES:
            raise ValueError("Status must be 'living', 'deceased', or 'unknown'")
        return v

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError("Age must be a positive integer")
        return v


class CharacterInDB(CharacterBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Character(CharacterInDB):
    pass
