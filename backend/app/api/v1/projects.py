from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.crud import project as crud_project
from app.schemas.project import ProjectCreate, ProjectUpdate, Project as ProjectSchema
from app.api.deps import get_current_user, get_project_for_view, get_project_for_modify
import logging

logger = logging.getLogger("thistory")

projects_bp = Blueprint('projects', __name__, url_prefix='/api/v1/projects')


@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        project_create = ProjectCreate(**data)
        new_project = crud_project.create_project(db.session, user.id, project_create)
        logger.info("Project created", extra={'user_id': user.id, 'project_id': new_project.id, 'operation': 'create_project'})
        return jsonify(ProjectSchema.model_validate(new_project).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating project: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('', methods=['GET'])
@jwt_required()
def list_projects():
    """List current user's projects"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        projects = crud_project.get_projects_by_user(db.session, user.id, skip, limit)
        return jsonify([ProjectSchema.model_validate(p).model_dump() for p in projects]), 200
    except Exception as e:
        logger.error(f"Error listing projects: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id: int):
    """Get a single project"""
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        return jsonify(ProjectSchema.model_validate(project).model_dump()), 200
    except Exception as e:
        logger.error(f"Error getting project: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id: int):
    """Update a project"""
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = request.get_json()
        project_update = ProjectUpdate(**data)
        updated_project = crud_project.update_project(db.session, project_id, project_update)
        logger.info("Project updated", extra={'user_id': user.id, 'project_id': project_id, 'operation': 'update_project'})
        return jsonify(ProjectSchema.model_validate(updated_project).model_dump()), 200
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating project: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id: int):
    """Delete a project"""
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        crud_project.delete_project(db.session, project_id)
        logger.info("Project deleted", extra={'user_id': user.id, 'project_id': project_id, 'operation': 'delete_project'})
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting project: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>/visibility', methods=['PATCH'])
@jwt_required()
def update_project_visibility(project_id: int):
    """Toggle project visibility"""
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = request.get_json()
        visibility = data.get('visibility')
        if visibility not in ['private', 'public']:
            return jsonify({"error": "Visibility must be 'private' or 'public'"}), 400
        project_update = ProjectUpdate(visibility=visibility)
        updated_project = crud_project.update_project(db.session, project_id, project_update)
        logger.info("Project visibility updated", extra={'user_id': user.id, 'project_id': project_id, 'operation': 'update_visibility', 'visibility': visibility})
        return jsonify(ProjectSchema.model_validate(updated_project).model_dump()), 200
    except Exception as e:
        logger.error(f"Error updating visibility: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


# Admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/projects', methods=['GET'])
@jwt_required()
def list_all_projects():
    """List all projects (admin only)"""
    try:
        user = get_current_user()
        if not user or not user.is_admin:
            return jsonify({"error": "Forbidden"}), 403
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        projects = crud_project.get_all_projects(db.session, skip, limit)
        return jsonify([ProjectSchema.model_validate(p).model_dump() for p in projects]), 200
    except Exception as e:
        logger.error(f"Error listing all projects: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
