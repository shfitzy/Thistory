import pytest
from app.database import db
from app.models.user import User
from app.models.project import Project
from app.models.location import Location
from app.models.race import Race
from app.models.character import Character
from app.models.event import Event
from app.crud import location as crud_location
from app.crud import race as crud_race
from app.crud import character as crud_character
from app.crud import event as crud_event
from app.schemas.location import LocationCreate, LocationUpdate
from app.schemas.race import RaceCreate, RaceUpdate
from app.schemas.character import CharacterCreate, CharacterUpdate
from app.schemas.event import EventCreate, EventUpdate


def make_user_and_project(suffix=""):
    user = User(email=f"user{suffix}@example.com", username=f"user{suffix}", hashed_password="hashed")
    db.session.add(user)
    db.session.flush()
    project = Project(user_id=user.id, title="Test Project", short_description="S", long_description="L")
    db.session.add(project)
    db.session.commit()
    return user, project


# --- Location CRUD ---

def test_create_location(app):
    with app.app_context():
        _, project = make_user_and_project()
        location = crud_location.create_location(db.session, project.id, LocationCreate(name="Rivendell"))
        assert location.id is not None
        assert location.name == "Rivendell"
        assert location.project_id == project.id


def test_get_location(app):
    with app.app_context():
        _, project = make_user_and_project()
        loc = Location(project_id=project.id, name="Mordor")
        db.session.add(loc)
        db.session.commit()
        result = crud_location.get_location(db.session, project.id, loc.id)
        assert result is not None
        assert result.name == "Mordor"


def test_list_locations_limit(app):
    with app.app_context():
        _, project = make_user_and_project()
        for i in range(5):
            db.session.add(Location(project_id=project.id, name=f"Place {i}"))
        db.session.commit()
        results = crud_location.list_locations(db.session, project.id, limit=3)
        assert len(results) == 3


def test_update_location(app):
    with app.app_context():
        _, project = make_user_and_project()
        loc = Location(project_id=project.id, name="Old Name")
        db.session.add(loc)
        db.session.commit()
        updated = crud_location.update_location(db.session, project.id, loc.id, LocationUpdate(name="New Name"))
        assert updated.name == "New Name"


def test_delete_location(app):
    with app.app_context():
        _, project = make_user_and_project()
        loc = Location(project_id=project.id, name="Temp")
        db.session.add(loc)
        db.session.commit()
        assert crud_location.delete_location(db.session, project.id, loc.id) is True
        assert crud_location.get_location(db.session, project.id, loc.id) is None


def test_location_scoped_to_project(app):
    with app.app_context():
        _, p1 = make_user_and_project("a")
        _, p2 = make_user_and_project("b")
        loc = Location(project_id=p1.id, name="Scoped")
        db.session.add(loc)
        db.session.commit()
        assert crud_location.get_location(db.session, p2.id, loc.id) is None


# --- Race CRUD ---

def test_create_race(app):
    with app.app_context():
        _, project = make_user_and_project()
        race = crud_race.create_race(db.session, project.id, RaceCreate(name="Elf"))
        assert race.id is not None
        assert race.name == "Elf"


def test_update_race(app):
    with app.app_context():
        _, project = make_user_and_project()
        race = Race(project_id=project.id, name="Dwarf")
        db.session.add(race)
        db.session.commit()
        updated = crud_race.update_race(db.session, project.id, race.id, RaceUpdate(description="<p>Stout folk</p>"))
        assert updated.description is not None


def test_delete_race(app):
    with app.app_context():
        _, project = make_user_and_project()
        race = Race(project_id=project.id, name="Orc")
        db.session.add(race)
        db.session.commit()
        assert crud_race.delete_race(db.session, project.id, race.id) is True
        assert crud_race.get_race(db.session, project.id, race.id) is None


# --- Character CRUD ---

def test_create_character(app):
    with app.app_context():
        _, project = make_user_and_project()
        char = crud_character.create_character(
            db.session, project.id,
            CharacterCreate(name="Aragorn", status="living", age=87)
        )
        assert char.id is not None
        assert char.status == "living"
        assert char.age == 87


def test_create_character_with_race(app):
    with app.app_context():
        _, project = make_user_and_project()
        race = Race(project_id=project.id, name="Human")
        db.session.add(race)
        db.session.commit()
        char = crud_character.create_character(
            db.session, project.id,
            CharacterCreate(name="Boromir", race_id=race.id)
        )
        assert char.race_id == race.id


def test_validate_race_in_project(app):
    with app.app_context():
        _, p1 = make_user_and_project("x")
        _, p2 = make_user_and_project("y")
        race = Race(project_id=p1.id, name="Elf")
        db.session.add(race)
        db.session.commit()
        assert crud_character.validate_race_in_project(db.session, p1.id, race.id) is True
        assert crud_character.validate_race_in_project(db.session, p2.id, race.id) is False


def test_update_character(app):
    with app.app_context():
        _, project = make_user_and_project()
        char = Character(project_id=project.id, name="Frodo")
        db.session.add(char)
        db.session.commit()
        updated = crud_character.update_character(
            db.session, project.id, char.id, CharacterUpdate(status="living", age=50)
        )
        assert updated.status == "living"
        assert updated.age == 50


def test_delete_character(app):
    with app.app_context():
        _, project = make_user_and_project()
        char = Character(project_id=project.id, name="Sauron")
        db.session.add(char)
        db.session.commit()
        assert crud_character.delete_character(db.session, project.id, char.id) is True


# --- Event CRUD ---

def test_create_event(app):
    with app.app_context():
        _, project = make_user_and_project()
        event = crud_event.create_event(
            db.session, project.id,
            EventCreate(name="Battle of Helm's Deep", event_date="Year 3019")
        )
        assert event.id is not None
        assert event.event_date == "Year 3019"


def test_create_event_with_end_date(app):
    with app.app_context():
        _, project = make_user_and_project()
        event = crud_event.create_event(
            db.session, project.id,
            EventCreate(name="War of the Ring", event_date="Year 3018", event_date_end="Year 3019")
        )
        assert event.event_date_end == "Year 3019"


def test_update_event(app):
    with app.app_context():
        _, project = make_user_and_project()
        event = Event(project_id=project.id, name="Old Event", event_date="Year 1")
        db.session.add(event)
        db.session.commit()
        updated = crud_event.update_event(
            db.session, project.id, event.id, EventUpdate(name="Updated Event")
        )
        assert updated.name == "Updated Event"


def test_delete_event(app):
    with app.app_context():
        _, project = make_user_and_project()
        event = Event(project_id=project.id, name="Temp Event", event_date="Year 0")
        db.session.add(event)
        db.session.commit()
        assert crud_event.delete_event(db.session, project.id, event.id) is True


# --- HTML Sanitization ---

def test_html_sanitization_on_create(app):
    with app.app_context():
        _, project = make_user_and_project()
        location = crud_location.create_location(
            db.session, project.id,
            LocationCreate(name="Dangerous", description='<p>Safe</p><script>alert("xss")</script>')
        )
        assert "<script>" not in (location.description or "")
        assert "<p>Safe</p>" in (location.description or "")


def test_html_sanitization_on_update(app):
    with app.app_context():
        _, project = make_user_and_project()
        loc = Location(project_id=project.id, name="Place")
        db.session.add(loc)
        db.session.commit()
        updated = crud_location.update_location(
            db.session, project.id, loc.id,
            LocationUpdate(description='<b>Bold</b><iframe src="evil.com"></iframe>')
        )
        assert "<iframe>" not in (updated.description or "")
        assert "<b>Bold</b>" in (updated.description or "")
