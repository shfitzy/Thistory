from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate
from app.utils.html_sanitizer import sanitize_html


def create_location(db: Session, project_id: int, data: LocationCreate) -> Location:
    location = Location(
        project_id=project_id,
        name=data.name,
        description=sanitize_html(data.description)
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def get_location(db: Session, project_id: int, location_id: int) -> Optional[Location]:
    return db.query(Location).filter(
        Location.id == location_id,
        Location.project_id == project_id
    ).first()


def list_locations(db: Session, project_id: int, skip: int = 0, limit: int = 50) -> List[Location]:
    return db.query(Location).filter(
        Location.project_id == project_id
    ).order_by(Location.created_at.desc()).offset(skip).limit(limit).all()


def update_location(db: Session, project_id: int, location_id: int, data: LocationUpdate) -> Optional[Location]:
    location = get_location(db, project_id, location_id)
    if not location:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if 'description' in update_data:
        update_data['description'] = sanitize_html(update_data['description'])
    for field, value in update_data.items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


def delete_location(db: Session, project_id: int, location_id: int) -> bool:
    location = get_location(db, project_id, location_id)
    if not location:
        return False
    db.delete(location)
    db.commit()
    return True
