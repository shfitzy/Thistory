from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from app.utils.html_sanitizer import sanitize_html


def create_event(db: Session, project_id: int, data: EventCreate) -> Event:
    event = Event(
        project_id=project_id,
        name=data.name,
        event_date=data.event_date,
        event_date_end=data.event_date_end,
        description=sanitize_html(data.description)
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_event(db: Session, project_id: int, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(
        Event.id == event_id,
        Event.project_id == project_id
    ).first()


def list_events(db: Session, project_id: int, skip: int = 0, limit: int = 50) -> List[Event]:
    return db.query(Event).filter(
        Event.project_id == project_id
    ).order_by(Event.event_date.asc()).offset(skip).limit(limit).all()


def update_event(db: Session, project_id: int, event_id: int, data: EventUpdate) -> Optional[Event]:
    event = get_event(db, project_id, event_id)
    if not event:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if 'description' in update_data:
        update_data['description'] = sanitize_html(update_data['description'])
    for field, value in update_data.items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, project_id: int, event_id: int) -> bool:
    event = get_event(db, project_id, event_id)
    if not event:
        return False
    db.delete(event)
    db.commit()
    return True
