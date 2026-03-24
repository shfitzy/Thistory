import pytest
from app.models.user import User
from app.models.project import Project
from app.database import db


def test_user_model_with_is_admin(app):
    """Test User model with is_admin field"""
    with app.app_context():
        # Create regular user
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed",
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.is_admin is False
        
        # Create admin user
        admin = User(
            email="admin@example.com",
            username="admin",
            hashed_password="hashed",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        assert admin.is_admin is True


def test_project_model_creation(app):
    """Test Project model creation"""
    with app.app_context():
        # Create user
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed"
        )
        db.session.add(user)
        db.session.commit()
        
        # Create project
        project = Project(
            user_id=user.id,
            title="Test Project",
            short_description="Short desc",
            long_description="Long description",
            visibility="private"
        )
        db.session.add(project)
        db.session.commit()
        
        assert project.id is not None
        assert project.user_id == user.id
        assert project.title == "Test Project"
        assert project.visibility == "private"


def test_project_user_relationship(app):
    """Test Project-User relationship"""
    with app.app_context():
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed"
        )
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="Test Project",
            short_description="Short",
            long_description="Long",
            visibility="private"
        )
        db.session.add(project)
        db.session.commit()
        
        # Test relationship
        assert project.owner.id == user.id
        assert len(user.projects) == 1
        assert user.projects[0].id == project.id


def test_project_cascade_delete(app):
    """Test cascade delete when user is deleted"""
    with app.app_context():
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed"
        )
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
        
        project_id = project.id
        
        # Delete user
        db.session.delete(user)
        db.session.commit()
        
        # Project should be deleted
        deleted_project = db.session.query(Project).filter(Project.id == project_id).first()
        assert deleted_project is None
