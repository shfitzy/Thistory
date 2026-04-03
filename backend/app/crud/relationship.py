from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from app.models.relationship import EntityRelationship
from app.schemas.relationship import RelationshipCreate


def create_relationship(db: Session, project_id: int, data: RelationshipCreate) -> EntityRelationship:
    relationship = EntityRelationship(
        project_id=project_id,
        from_entity_type=data.from_entity_type,
        from_entity_id=data.from_entity_id,
        to_entity_type=data.to_entity_type,
        to_entity_id=data.to_entity_id,
        relationship_type=data.relationship_type,
        description=data.description
    )
    db.add(relationship)
    db.commit()
    db.refresh(relationship)
    return relationship


def get_relationships(db: Session, project_id: int, entity_type: str, entity_id: int) -> List[EntityRelationship]:
    """Get all relationships where entity is source or target."""
    return db.query(EntityRelationship).filter(
        EntityRelationship.project_id == project_id,
        db.query(EntityRelationship).filter(
            ((EntityRelationship.from_entity_type == entity_type) & (EntityRelationship.from_entity_id == entity_id)) |
            ((EntityRelationship.to_entity_type == entity_type) & (EntityRelationship.to_entity_id == entity_id))
        ).exists()
    ).all()


def get_relationships_for_entity(db: Session, project_id: int, entity_type: str, entity_id: int) -> List[EntityRelationship]:
    return db.query(EntityRelationship).filter(
        EntityRelationship.project_id == project_id,
        (
            ((EntityRelationship.from_entity_type == entity_type) & (EntityRelationship.from_entity_id == entity_id)) |
            ((EntityRelationship.to_entity_type == entity_type) & (EntityRelationship.to_entity_id == entity_id))
        )
    ).all()


def get_relationship(db: Session, project_id: int, relationship_id: int) -> Optional[EntityRelationship]:
    return db.query(EntityRelationship).filter(
        EntityRelationship.id == relationship_id,
        EntityRelationship.project_id == project_id
    ).first()


def delete_relationship(db: Session, project_id: int, relationship_id: int) -> bool:
    relationship = get_relationship(db, project_id, relationship_id)
    if not relationship:
        return False
    db.delete(relationship)
    db.commit()
    return True


def check_duplicate(db: Session, project_id: int, data: RelationshipCreate) -> bool:
    return db.query(EntityRelationship).filter(
        EntityRelationship.project_id == project_id,
        EntityRelationship.from_entity_type == data.from_entity_type,
        EntityRelationship.from_entity_id == data.from_entity_id,
        EntityRelationship.to_entity_type == data.to_entity_type,
        EntityRelationship.to_entity_id == data.to_entity_id
    ).first() is not None
