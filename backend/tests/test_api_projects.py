import pytest
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.models.project import Project
from app.database import db


def test_create_project_api(client, app):
    """Test POST /api/v1/projects (Story 1)"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id))
        
        response = client.post(
            '/api/v1/projects',
            json={
                'title': 'New Project',
                'short_description': 'Short desc',
                'long_description': 'Long description',
                'visibility': 'private'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'New Project'
        assert data['user_id'] == user.id


def test_list_projects_api(client, app):
    """Test GET /api/v1/projects (Story 2)"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="Test Project",
            short_description="Short",
            long_description="Long"
        )
        db.session.add(project)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id))
        
        response = client.get(
            '/api/v1/projects',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
        assert data[0]['title'] == 'Test Project'


def test_get_project_api_owner(client, app):
    """Test GET /api/v1/projects/{id} as owner (Story 2)"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="Test",
            short_description="Short",
            long_description="Long",
            visibility="private"
        )
        db.session.add(project)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id))
        
        response = client.get(
            f'/api/v1/projects/{project.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == project.id


def test_get_project_api_unauthorized(client, app):
    """Test GET /api/v1/projects/{id} unauthorized returns 404 (Story 2)"""
    with app.app_context():
        owner = User(email="owner@example.com", username="owner", hashed_password="hashed")
        other_user = User(email="other@example.com", username="other", hashed_password="hashed")
        db.session.add_all([owner, other_user])
        db.session.commit()
        
        project = Project(
            user_id=owner.id,
            title="Private Project",
            short_description="Short",
            long_description="Long",
            visibility="private"
        )
        db.session.add(project)
        db.session.commit()
        
        token = create_access_token(identity=str(other_user.id))
        
        response = client.get(
            f'/api/v1/projects/{project.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Should return 404 to not reveal existence
        assert response.status_code == 404


def test_get_public_project_api(client, app):
    """Test GET /api/v1/projects/{id} for public project (Story 2)"""
    with app.app_context():
        owner = User(email="owner@example.com", username="owner", hashed_password="hashed")
        other_user = User(email="other@example.com", username="other", hashed_password="hashed")
        db.session.add_all([owner, other_user])
        db.session.commit()
        
        project = Project(
            user_id=owner.id,
            title="Public Project",
            short_description="Short",
            long_description="Long",
            visibility="public"
        )
        db.session.add(project)
        db.session.commit()
        
        token = create_access_token(identity=str(other_user.id))
        
        response = client.get(
            f'/api/v1/projects/{project.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200


def test_update_project_api(client, app):
    """Test PUT /api/v1/projects/{id} (Story 3)"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="Original",
            short_description="Short",
            long_description="Long"
        )
        db.session.add(project)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id))
        
        response = client.put(
            f'/api/v1/projects/{project.id}',
            json={'title': 'Updated Title'},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Title'


def test_delete_project_api(client, app):
    """Test DELETE /api/v1/projects/{id} (Story 4)"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="To Delete",
            short_description="Short",
            long_description="Long"
        )
        db.session.add(project)
        db.session.commit()
        
        project_id = project.id
        token = create_access_token(identity=str(user.id))
        
        response = client.delete(
            f'/api/v1/projects/{project_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 204
        
        # Verify deleted
        get_response = client.get(
            f'/api/v1/projects/{project_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert get_response.status_code == 404


def test_update_visibility_api(client, app):
    """Test PATCH /api/v1/projects/{id}/visibility (Story 5)"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="Test",
            short_description="Short",
            long_description="Long",
            visibility="private"
        )
        db.session.add(project)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id))
        
        response = client.patch(
            f'/api/v1/projects/{project.id}/visibility',
            json={'visibility': 'public'},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['visibility'] == 'public'


def test_admin_list_all_projects_api(client, app):
    """Test GET /api/v1/admin/projects (Story 6)"""
    with app.app_context():
        admin = User(email="admin@example.com", username="admin", hashed_password="hashed", is_admin=True)
        user = User(email="user@example.com", username="user", hashed_password="hashed")
        db.session.add_all([admin, user])
        db.session.commit()
        
        project1 = Project(user_id=admin.id, title="Admin Project", short_description="S", long_description="L")
        project2 = Project(user_id=user.id, title="User Project", short_description="S", long_description="L", visibility="private")
        db.session.add_all([project1, project2])
        db.session.commit()
        
        token = create_access_token(identity=str(admin.id))
        
        response = client.get(
            '/api/v1/admin/projects',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 2


def test_non_admin_cannot_list_all_projects(client, app):
    """Test non-admin cannot access admin endpoint (Story 6)"""
    with app.app_context():
        user = User(email="user@example.com", username="user", hashed_password="hashed", is_admin=False)
        db.session.add(user)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id))
        
        response = client.get(
            '/api/v1/admin/projects',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 403


def test_authentication_required(client):
    """Test authentication is required for all endpoints"""
    response = client.get('/api/v1/projects')
    assert response.status_code == 401
    
    response = client.post('/api/v1/projects', json={})
    assert response.status_code == 401
