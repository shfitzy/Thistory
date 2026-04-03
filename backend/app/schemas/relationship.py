from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

VALID_ENTITY_TYPES = {'location', 'race', 'character', 'event'}


class RelationshipCreate(BaseModel):
    from_entity_type: str
    from_entity_id: int
    to_entity_type: str
    to_entity_id: int
    relationship_type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

    @model_validator(mode='after')
    def validate_relationship(self):
        if self.from_entity_type not in VALID_ENTITY_TYPES:
            raise ValueError(f"from_entity_type must be one of {VALID_ENTITY_TYPES}")
        if self.to_entity_type not in VALID_ENTITY_TYPES:
            raise ValueError(f"to_entity_type must be one of {VALID_ENTITY_TYPES}")
        if self.from_entity_type == self.to_entity_type and self.from_entity_id == self.to_entity_id:
            raise ValueError("Cannot relate an entity to itself")
        return self


class RelationshipInDB(RelationshipCreate):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Relationship(RelationshipInDB):
    pass
