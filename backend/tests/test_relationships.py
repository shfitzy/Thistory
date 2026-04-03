import pytest
from flask_jwt_extended import create_access_token
from app.database import db
from app.models.user import User
from app.models.project import Project
from app.models.location import Location
from app.models.character import Character
from app.models.relationship import EntityRelationship
from app.crud import relationship as crud_relationship
from app.schemas.relationship import RelationshipCreate


def make_user_project_token(suffix=""):
    user = User(email=f"user{suffix}@example.com", username=f"user{suffix}", hashed_password="hashed")
    db.session.add(user)
    db.session.flush()
    project = Project(user_id=user.id, title="Test Project", short_description="S", long_description="L")
    db.session.add(project)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return user, project, token


# --- CRUD ---

def test_create_relationship(app):
    with app.app_context():
        _, project, _ = make_user_project_token()
        data = RelationshipCreate(
            from_entity_type="character",
            from_entity_id=1,
            to_entity_type="location",
            to_entity_id=2,
            relationship_type="lives_in"
        )
        rel = crud_relationship.create_relationship(db.session, project.id, data)
        assert rel.id is not None
        assert rel.relationship_type == "lives_in"


def test_get_relationships_for_entity(app):
    with app.app_context():
        _, project, _ = make_user_project_token()
        rel = EntityRelationship(
            project_id=project.id,
            from_entity_type="character", from_entity_id=1,
            to_entity_type="location", to_entity_id=2
        )
        db.session.add(rel)
        db.session.commit()
        results = crud_relationship.get_relationships_for_entity(db.session, project.id, "character", 1)
        assert len(results) == 1
        # Also found when querying from the other side
        results2 = crud_relationship.get_relationships_for_entity(db.session, project.id, "location", 2)
        assert len(results2) == 1


def test_delete_relationship(app):
    with app.app_context():
        _, project, _ = make_user_project_token()
        rel = EntityRelationship(
            project_id=project.id,
            from_entity_type="race", from_entity_id=1,
            to_entity_type="character", to_entity_id=2
        )
        db.session.add(rel)
        db.session.commit()
        assert crud_relationship.delete_relationship(db.session, project.id, rel.id) is True
        assert crud_relationship.get_relationship(db.session, project.id, rel.id) is None


def test_check_duplicate(app):
    with app.app_context():
        _, project, _ = make_user_project_token()
        data = RelationshipCreate(
            from_entity_type="character", from_entity_id=1,
            to_entity_type="location", to_entity_id=2
        )
        crud_relationship.create_relationship(db.session, project.id, data)
        assert crud_relationship.check_duplicate(db.session, project.id, data) is True


# --- Schema validation ---

def test_self_relationship_rejected():
    with pytest.raises(ValueError, match="Cannot relate an entity to itself"):
        RelationshipCreate(
            from_entity_type="character", from_entity_id=1,
            to_entity_type="character", to_entity_id=1
        )


def test_invalid_entity_type_rejected():
    with pytest.raises(ValueError):
        RelationshipCreate(
            from_entity_type="dragon", from_entity_id=1,
            to_entity_type="character", to_entity_id=2
        )


# --- API ---

def test_create_relationship_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token()
        response = client.post(
            f'/api/v1/projects/{project.id}/relationships',
            json={
                'from_entity_type': 'character',
                'from_entity_id': 1,
                'to_entity_type': 'location',
                'to_entity_id': 2,
                'relationship_type': 'lives_in'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        assert response.get_json()['relationship_type'] == 'lives_in'


def test_duplicate_relationship_returns_400(client, app):
    with app.app_context():
        _, project, token = make_user_project_token()
        payload = {
            'from_entity_type': 'character',
            'from_entity_id': 1,
            'to_entity_type': 'location',
            'to_entity_id': 2
        }
        client.post(
            f'/api/v1/projects/{project.id}/relationships',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        response = client.post(
            f'/api/v1/projects/{project.id}/relationships',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400
        assert 'already exists' in response.get_json()['error']


def test_self_relationship_returns_400(client, app):
    with app.app_context():
        _, project, token = make_user_project_token()
        response = client.post(
            f'/api/v1/projects/{project.id}/relationships',
            json={
                'from_entity_type': 'character',
                'from_entity_id': 1,
                'to_entity_type': 'character',
                'to_entity_id': 1
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400


def test_list_relationships_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token()
        rel = EntityRelationship(
            project_id=project.id,
            from_entity_type="character", from_entity_id=5,
            to_entity_type="location", to_entity_id=10
        )
        db.session.add(rel)
        db.session.commit()
        response = client.get(
            f'/api/v1/projects/{project.id}/relationships?entity_type=character&entity_id=5',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert len(response.get_json()) == 1


def test_delete_relationship_api(client, app):
    with app.app_context():
        _, project, token = make_user_project_token()
        rel = EntityRelationship(
            project_id=project.id,
            from_entity_type="race", from_entity_id=1,
            to_entity_type="character", to_entity_id=2
        )
        db.session.add(rel)
        db.session.commit()
        response = client.delete(
            f'/api/v1/projects/{project.id}/relationships/{rel.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 204


def test_list_relationships_missing_params(client, app):
    with app.app_context():
        _, project, token = make_user_project_token()
        response = client.get(
            f'/api/v1/projects/{project.id}/relationships',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400
