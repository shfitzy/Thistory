from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    short_description: str = Field(..., min_length=1, max_length=500)
    long_description: str = Field(..., min_length=1)
    visibility: str = Field(default="private")

    @field_validator('title', 'short_description', 'long_description')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator('visibility')
    @classmethod
    def validate_visibility(cls, v):
        if v not in ['private', 'public']:
            raise ValueError("Visibility must be 'private' or 'public'")
        return v


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    short_description: Optional[str] = Field(None, min_length=1, max_length=500)
    long_description: Optional[str] = Field(None, min_length=1)
    visibility: Optional[str] = None

    @field_validator('title', 'short_description', 'long_description')
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip() if isinstance(v, str) and v else v

    @field_validator('visibility')
    @classmethod
    def validate_visibility(cls, v):
        if v is not None and v not in ['private', 'public']:
            raise ValueError("Visibility must be 'private' or 'public'")
        return v


class ProjectInDB(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Project(ProjectInDB):
    pass
