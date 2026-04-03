import pytest
from flask_jwt_extended import create_access_token
from app.database import db
from app.models.user import User
from app.models.project import Project
from app.models.location import Location
from app.models.race import Race
from app.models.character import Character
from app.models.event import Event


def make_user_project_token(app, suffix=""):
    user = User(email=f"user{suffix}@example.com", username=f"user{suffix}", hashed_password="hashed")
    db.session.add(user)
    db.session.flush()
    project = Project(user_id=user.id, title="Test Project", short_description="S", long_description="L")
    db.session.add(project)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return user, project, token


# --- Locations API ---

def test_create_location_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        response = client.post(
            f'/api/v1/projects/{project.id}/locations',
            json={'name': 'Rivendell'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        assert response.get_json()['name'] == 'Rivendell'


def test_list_locations_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        db.session.add(Location(project_id=project.id, name="Mordor"))
        db.session.commit()
        response = client.get(
            f'/api/v1/projects/{project.id}/locations',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert len(response.get_json()) == 1


def test_get_location_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        loc = Location(project_id=project.id, name="Shire")
        db.session.add(loc)
        db.session.commit()
        response = client.get(
            f'/api/v1/projects/{project.id}/locations/{loc.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.get_json()['name'] == 'Shire'


def test_update_location_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        loc = Location(project_id=project.id, name="Old")
        db.session.add(loc)
        db.session.commit()
        response = client.put(
            f'/api/v1/projects/{project.id}/locations/{loc.id}',
            json={'name': 'New'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.get_json()['name'] == 'New'


def test_delete_location_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        loc = Location(project_id=project.id, name="Temp")
        db.session.add(loc)
        db.session.commit()
        response = client.delete(
            f'/api/v1/projects/{project.id}/locations/{loc.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 204


def test_location_not_found_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        response = client.get(
            f'/api/v1/projects/{project.id}/locations/9999',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 404


# --- Races API ---

def test_create_race_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        response = client.post(
            f'/api/v1/projects/{project.id}/races',
            json={'name': 'Elf'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        assert response.get_json()['name'] == 'Elf'


def test_delete_race_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        race = Race(project_id=project.id, name="Orc")
        db.session.add(race)
        db.session.commit()
        response = client.delete(
            f'/api/v1/projects/{project.id}/races/{race.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 204


# --- Characters API ---

def test_create_character_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        response = client.post(
            f'/api/v1/projects/{project.id}/characters',
            json={'name': 'Gandalf', 'status': 'living'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        assert response.get_json()['name'] == 'Gandalf'


def test_create_character_invalid_race_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        response = client.post(
            f'/api/v1/projects/{project.id}/characters',
            json={'name': 'Legolas', 'race_id': 9999},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400


def test_update_character_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        char = Character(project_id=project.id, name="Bilbo")
        db.session.add(char)
        db.session.commit()
        response = client.put(
            f'/api/v1/projects/{project.id}/characters/{char.id}',
            json={'age': 111},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.get_json()['age'] == 111


# --- Events API ---

def test_create_event_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        response = client.post(
            f'/api/v1/projects/{project.id}/events',
            json={'name': 'Council of Elrond', 'event_date': 'Year 3018'},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        assert response.get_json()['event_date'] == 'Year 3018'


def test_list_events_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token(app)
        db.session.add(Event(project_id=project.id, name="Event A", event_date="Year 1"))
        db.session.add(Event(project_id=project.id, name="Event B", event_date="Year 2"))
        db.session.commit()
        response = client.get(
            f'/api/v1/projects/{project.id}/events',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert len(response.get_json()) == 2


# --- Access control ---

def test_other_user_cannot_access_content(client, app):
    with app.app_context():
        _, project, _ = make_user_project_token(app, "owner")
        other = User(email="other@example.com", username="other", hashed_password="hashed")
        db.session.add(other)
        db.session.commit()
        other_token = create_access_token(identity=str(other.id))
        response = client.get(
            f'/api/v1/projects/{project.id}/locations',
            headers={'Authorization': f'Bearer {other_token}'}
        )
        assert response.status_code == 404


def test_unauthenticated_cannot_access_content(client, app):
    with app.app_context():
        _, project, _ = make_user_project_token(app)
        response = client.get(f'/api/v1/projects/{project.id}/locations')
        assert response.status_code == 401
