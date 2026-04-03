from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import db
from app.crud import relationship as crud_relationship
from app.schemas.relationship import RelationshipCreate, Relationship as RelationshipSchema
from app.api.deps import get_project_for_view, get_project_for_modify
import logging

logger = logging.getLogger("thistory")

relationships_bp = Blueprint('relationships', __name__, url_prefix='/api/v1/projects/<int:project_id>/relationships')


@relationships_bp.route('', methods=['GET'])
@jwt_required()
def list_relationships(project_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        entity_type = request.args.get('entity_type')
        entity_id = request.args.get('entity_id', type=int)
        if not entity_type or entity_id is None:
            return jsonify({"error": "entity_type and entity_id query params are required"}), 400
        relationships = crud_relationship.get_relationships_for_entity(db.session, project_id, entity_type, entity_id)
        return jsonify([RelationshipSchema.model_validate(r).model_dump() for r in relationships]), 200
    except Exception as e:
        logger.error(f"Error listing relationships: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@relationships_bp.route('', methods=['POST'])
@jwt_required()
def create_relationship(project_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = RelationshipCreate(**request.get_json())
        if crud_relationship.check_duplicate(db.session, project_id, data):
            return jsonify({"error": "Relationship already exists"}), 400
        relationship = crud_relationship.create_relationship(db.session, project_id, data)
        logger.info("Relationship created", extra={'user_id': user.id, 'project_id': project_id, 'relationship_id': relationship.id})
        return jsonify(RelationshipSchema.model_validate(relationship).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating relationship: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@relationships_bp.route('/<int:relationship_id>', methods=['DELETE'])
@jwt_required()
def delete_relationship(project_id: int, relationship_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        if not crud_relationship.delete_relationship(db.session, project_id, relationship_id):
            return jsonify({"error": "Not found"}), 404
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting relationship: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
