from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.models.project import Project
from app.database import db
from typing import Optional, Tuple


def get_current_user() -> Optional[User]:
    """Get the current authenticated user."""
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.filter_by(id=int(user_id)).first()


def can_view_project(project: Project, user: User) -> bool:
    """Check if a user can view a project and its children.

    Currently allows: project owner, admin users.
    Extend this method to add additional view access rules.
    """
    if user.is_admin:
        return True
    if project.user_id == user.id:
        return True
    return False


def can_modify_project(project: Project, user: User) -> bool:
    """Check if a user can create/update/delete content within a project.

    Currently allows: project owner only.
    Extend this method to add additional modify access rules (e.g. admin, collaborators).
    """
    if project.user_id == user.id:
        return True
    return False


def get_project_for_view(project_id: int) -> Tuple[Optional[Project], Optional[User], Optional[tuple]]:
    """Gate: load project and verify the current user has view access.

    Returns (project, user, error_response). If error_response is not None,
    return it directly from the route handler.
    """
    user = get_current_user()
    if not user:
        return None, None, (jsonify({"error": "Unauthorized"}), 401)

    project = db.session.get(Project, project_id)
    if not project or not can_view_project(project, user):
        return None, None, (jsonify({"error": "Not found"}), 404)

    return project, user, None


def get_project_for_modify(project_id: int) -> Tuple[Optional[Project], Optional[User], Optional[tuple]]:
    """Gate: load project and verify the current user has modify access.

    Returns (project, user, error_response). If error_response is not None,
    return it directly from the route handler.
    """
    user = get_current_user()
    if not user:
        return None, None, (jsonify({"error": "Unauthorized"}), 401)

    project = db.session.get(Project, project_id)
    if not project or not can_modify_project(project, user):
        return None, None, (jsonify({"error": "Not found"}), 404)

    return project, user, None
