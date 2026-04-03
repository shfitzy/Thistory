from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate
from app.utils.html_sanitizer import sanitize_html


def create_character(db: Session, project_id: int, data: CharacterCreate) -> Character:
    character = Character(
        project_id=project_id,
        name=data.name,
        status=data.status,
        age=data.age,
        race_id=data.race_id,
        description=sanitize_html(data.description)
    )
    db.add(character)
    db.commit()
    db.refresh(character)
    return character


def get_character(db: Session, project_id: int, character_id: int) -> Optional[Character]:
    return db.query(Character).filter(
        Character.id == character_id,
        Character.project_id == project_id
    ).first()


def list_characters(db: Session, project_id: int, skip: int = 0, limit: int = 50) -> List[Character]:
    return db.query(Character).filter(
        Character.project_id == project_id
    ).order_by(Character.created_at.desc()).offset(skip).limit(limit).all()


def update_character(db: Session, project_id: int, character_id: int, data: CharacterUpdate) -> Optional[Character]:
    character = get_character(db, project_id, character_id)
    if not character:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if 'description' in update_data:
        update_data['description'] = sanitize_html(update_data['description'])
    for field, value in update_data.items():
        setattr(character, field, value)
    db.commit()
    db.refresh(character)
    return character


def delete_character(db: Session, project_id: int, character_id: int) -> bool:
    character = get_character(db, project_id, character_id)
    if not character:
        return False
    db.delete(character)
    db.commit()
    return True


def validate_race_in_project(db: Session, project_id: int, race_id: int) -> bool:
    """Verify a race belongs to the same project before assigning to a character."""
    from app.models.race import Race
    return db.query(Race).filter(
        Race.id == race_id,
        Race.project_id == project_id
    ).first() is not None
