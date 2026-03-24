from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from app.database import db
from app.crud import project as crud_project
from app.crud import user as crud_user
from app.schemas.project import ProjectCreate, ProjectUpdate, Project as ProjectSchema
from typing import List
import logging

logger = logging.getLogger("thistory")

projects_bp = Blueprint('projects', __name__, url_prefix='/api/v1/projects')


@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project (Story 1)"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate input
        project_create = ProjectCreate(**data)
        
        # Create project
        new_project = crud_project.create_project(db.session, user_id, project_create)
        
        logger.info(f"Project created", extra={'user_id': user_id, 'project_id': new_project.id, 'operation': 'create_project'})
        
        return jsonify(ProjectSchema.model_validate(new_project).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}", extra={'user_id': user_id}, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('', methods=['GET'])
@jwt_required()
def list_projects():
    """List user's projects (Story 2)"""
    try:
        user_id = int(get_jwt_identity())
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        projects = crud_project.get_projects_by_user(db.session, user_id, skip, limit)
        
        return jsonify([ProjectSchema.model_validate(p).model_dump() for p in projects]), 200
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}", extra={'user_id': user_id}, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id: int):
    """Get a single project (Story 2)"""
    try:
        user_id = int(get_jwt_identity())
        user = crud_user.get_user(user_id)
        
        project = crud_project.get_project(db.session, project_id)
        
        # Check access
        if not project or not crud_project.check_project_access(project, user_id, user.is_admin):
            return jsonify({"error": "Not found"}), 404
        
        return jsonify(ProjectSchema.model_validate(project).model_dump()), 200
    except Exception as e:
        logger.error(f"Error getting project: {str(e)}", extra={'user_id': user_id, 'project_id': project_id}, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id: int):
    """Update a project (Story 3)"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate input
        project_update = ProjectUpdate(**data)
        
        # Get project
        project = crud_project.get_project(db.session, project_id)
        
        # Check modify access (owner only)
        if not project or not crud_project.check_project_modify_access(project, user_id):
            return jsonify({"error": "Not found"}), 404
        
        # Update project
        updated_project = crud_project.update_project(db.session, project_id, project_update)
        
        logger.info(f"Project updated", extra={'user_id': user_id, 'project_id': project_id, 'operation': 'update_project'})
        
        return jsonify(ProjectSchema.model_validate(updated_project).model_dump()), 200
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}", extra={'user_id': user_id, 'project_id': project_id}, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id: int):
    """Delete a project (Story 4)"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get project
        project = crud_project.get_project(db.session, project_id)
        
        # Check modify access (owner only)
        if not project or not crud_project.check_project_modify_access(project, user_id):
            return jsonify({"error": "Not found"}), 404
        
        # Delete project
        crud_project.delete_project(db.session, project_id)
        
        logger.info(f"Project deleted", extra={'user_id': user_id, 'project_id': project_id, 'operation': 'delete_project'})
        
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}", extra={'user_id': user_id, 'project_id': project_id}, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@projects_bp.route('/<int:project_id>/visibility', methods=['PATCH'])
@jwt_required()
def update_project_visibility(project_id: int):
    """Toggle project visibility (Story 5)"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        visibility = data.get('visibility')
        
        if visibility not in ['private', 'public']:
            return jsonify({"error": "Visibility must be 'private' or 'public'"}), 400
        
        # Get project
        project = crud_project.get_project(db.session, project_id)
        
        # Check modify access (owner only)
        if not project or not crud_project.check_project_modify_access(project, user_id):
            return jsonify({"error": "Not found"}), 404
        
        # Update visibility
        project_update = ProjectUpdate(visibility=visibility)
        updated_project = crud_project.update_project(db.session, project_id, project_update)
        
        logger.info(f"Project visibility updated", extra={'user_id': user_id, 'project_id': project_id, 'operation': 'update_visibility', 'visibility': visibility})
        
        return jsonify(ProjectSchema.model_validate(updated_project).model_dump()), 200
    except Exception as e:
        logger.error(f"Error updating visibility: {str(e)}", extra={'user_id': user_id, 'project_id': project_id}, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


# Admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/projects', methods=['GET'])
@jwt_required()
def list_all_projects():
    """List all projects (admin only, Story 6)"""
    try:
        user_id = int(get_jwt_identity())
        user = crud_user.get_user(user_id)
        
        # Check admin access
        if not user or not user.is_admin:
            return jsonify({"error": "Forbidden"}), 403
        
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        projects = crud_project.get_all_projects(db.session, skip, limit)
        
        return jsonify([ProjectSchema.model_validate(p).model_dump() for p in projects]), 200
    except Exception as e:
        logger.error(f"Error listing all projects: {str(e)}", extra={'user_id': user_id}, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
