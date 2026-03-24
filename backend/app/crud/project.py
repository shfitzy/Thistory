from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from typing import Optional, List


def create_project(db: Session, user_id: int, project: ProjectCreate) -> Project:
    """Create a new project for a user"""
    db_project = Project(
        user_id=user_id,
        title=project.title.strip(),
        short_description=project.short_description.strip(),
        long_description=project.long_description.strip(),
        visibility=project.visibility
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int) -> Optional[Project]:
    """Get a project by ID"""
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
    """Get all projects for a specific user"""
    return db.query(Project).filter(Project.user_id == user_id).offset(skip).limit(limit).all()


def get_all_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """Get all projects (admin only)"""
    return db.query(Project).offset(skip).limit(limit).all()


def update_project(db: Session, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
    """Update a project"""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    update_data = project_update.model_dump(exclude_unset=True)
    
    # Strip whitespace from text fields
    if 'title' in update_data and update_data['title']:
        update_data['title'] = update_data['title'].strip()
    if 'short_description' in update_data and update_data['short_description']:
        update_data['short_description'] = update_data['short_description'].strip()
    if 'long_description' in update_data and update_data['long_description']:
        update_data['long_description'] = update_data['long_description'].strip()
    
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    """Delete a project (cascade deletes all related content)"""
    db_project = get_project(db, project_id)
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True


def check_project_access(project: Project, user_id: int, is_admin: bool) -> bool:
    """Check if user has access to view a project"""
    if is_admin:
        return True
    if project.user_id == user_id:
        return True
    if project.visibility == 'public':
        return True
    return False


def check_project_modify_access(project: Project, user_id: int) -> bool:
    """Check if user can modify a project (owner only)"""
    return project.user_id == user_id
