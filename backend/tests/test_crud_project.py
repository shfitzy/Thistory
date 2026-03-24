import pytest
from app.crud import project as crud_project
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.database import db


def test_create_project(app):
    """Test create_project CRUD operation"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project_data = ProjectCreate(
            title="Test Project",
            short_description="Short description",
            long_description="Long description",
            visibility="private"
        )
        
        project = crud_project.create_project(db.session, user.id, project_data)
        
        assert project.id is not None
        assert project.user_id == user.id
        assert project.title == "Test Project"
        assert project.visibility == "private"


def test_get_project(app):
    """Test get_project CRUD operation"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="Test",
            short_description="Short",
            long_description="Long"
        )
        db.session.add(project)
        db.session.commit()
        
        retrieved = crud_project.get_project(db.session, project.id)
        
        assert retrieved is not None
        assert retrieved.id == project.id


def test_get_projects_by_user(app):
    """Test get_projects_by_user CRUD operation"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        for i in range(3):
            project = Project(
                user_id=user.id,
                title=f"Project {i}",
                short_description="Short",
                long_description="Long"
            )
            db.session.add(project)
        db.session.commit()
        
        projects = crud_project.get_projects_by_user(db.session, user.id)
        
        assert len(projects) == 3


def test_get_all_projects_admin(app):
    """Test get_all_projects CRUD operation (admin)"""
    with app.app_context():
        user1 = User(email="user1@example.com", username="user1", hashed_password="hashed")
        user2 = User(email="user2@example.com", username="user2", hashed_password="hashed")
        db.session.add_all([user1, user2])
        db.session.commit()
        
        project1 = Project(user_id=user1.id, title="P1", short_description="S", long_description="L")
        project2 = Project(user_id=user2.id, title="P2", short_description="S", long_description="L")
        db.session.add_all([project1, project2])
        db.session.commit()
        
        all_projects = crud_project.get_all_projects(db.session)
        
        assert len(all_projects) >= 2


def test_update_project(app):
    """Test update_project CRUD operation"""
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
        
        update_data = ProjectUpdate(title="Updated Title")
        updated = crud_project.update_project(db.session, project.id, update_data)
        
        assert updated.title == "Updated Title"
        assert updated.short_description == "Short"  # Unchanged


def test_delete_project(app):
    """Test delete_project CRUD operation"""
    with app.app_context():
        user = User(email="test@example.com", username="testuser", hashed_password="hashed")
        db.session.add(user)
        db.session.commit()
        
        project = Project(
            user_id=user.id,
            title="Test",
            short_description="Short",
            long_description="Long"
        )
        db.session.add(project)
        db.session.commit()
        
        project_id = project.id
        result = crud_project.delete_project(db.session, project_id)
        
        assert result is True
        assert crud_project.get_project(db.session, project_id) is None


def test_check_project_access(app):
    """Test check_project_access function"""
    with app.app_context():
        owner = User(email="owner@example.com", username="owner", hashed_password="hashed")
        other_user = User(email="other@example.com", username="other", hashed_password="hashed")
        admin = User(email="admin@example.com", username="admin", hashed_password="hashed", is_admin=True)
        db.session.add_all([owner, other_user, admin])
        db.session.commit()
        
        private_project = Project(
            user_id=owner.id,
            title="Private",
            short_description="S",
            long_description="L",
            visibility="private"
        )
        public_project = Project(
            user_id=owner.id,
            title="Public",
            short_description="S",
            long_description="L",
            visibility="public"
        )
        db.session.add_all([private_project, public_project])
        db.session.commit()
        
        # Owner can access private project
        assert crud_project.check_project_access(private_project, owner.id, False) is True
        
        # Other user cannot access private project
        assert crud_project.check_project_access(private_project, other_user.id, False) is False
        
        # Other user can access public project
        assert crud_project.check_project_access(public_project, other_user.id, False) is True
        
        # Admin can access private project
        assert crud_project.check_project_access(private_project, admin.id, True) is True


def test_check_project_modify_access(app):
    """Test check_project_modify_access function"""
    with app.app_context():
        owner = User(email="owner@example.com", username="owner", hashed_password="hashed")
        other_user = User(email="other@example.com", username="other", hashed_password="hashed")
        db.session.add_all([owner, other_user])
        db.session.commit()
        
        project = Project(
            user_id=owner.id,
            title="Test",
            short_description="S",
            long_description="L"
        )
        db.session.add(project)
        db.session.commit()
        
        # Owner can modify
        assert crud_project.check_project_modify_access(project, owner.id) is True
        
        # Other user cannot modify
        assert crud_project.check_project_modify_access(project, other_user.id) is False
