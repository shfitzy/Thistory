from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.race import Race
from app.schemas.race import RaceCreate, RaceUpdate
from app.utils.html_sanitizer import sanitize_html


def create_race(db: Session, project_id: int, data: RaceCreate) -> Race:
    race = Race(
        project_id=project_id,
        name=data.name,
        description=sanitize_html(data.description)
    )
    db.add(race)
    db.commit()
    db.refresh(race)
    return race


def get_race(db: Session, project_id: int, race_id: int) -> Optional[Race]:
    return db.query(Race).filter(
        Race.id == race_id,
        Race.project_id == project_id
    ).first()


def list_races(db: Session, project_id: int, skip: int = 0, limit: int = 50) -> List[Race]:
    return db.query(Race).filter(
        Race.project_id == project_id
    ).order_by(Race.created_at.desc()).offset(skip).limit(limit).all()


def update_race(db: Session, project_id: int, race_id: int, data: RaceUpdate) -> Optional[Race]:
    race = get_race(db, project_id, race_id)
    if not race:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if 'description' in update_data:
        update_data['description'] = sanitize_html(update_data['description'])
    for field, value in update_data.items():
        setattr(race, field, value)
    db.commit()
    db.refresh(race)
    return race


def delete_race(db: Session, project_id: int, race_id: int) -> bool:
    race = get_race(db, project_id, race_id)
    if not race:
        return False
    db.delete(race)
    db.commit()
    return True
