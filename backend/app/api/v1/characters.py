from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import db
from app.crud import character as crud_character
from app.schemas.character import CharacterCreate, CharacterUpdate, Character as CharacterSchema
from app.api.deps import get_project_for_view, get_project_for_modify
import logging

logger = logging.getLogger("thistory")

characters_bp = Blueprint('characters', __name__, url_prefix='/api/v1/projects/<int:project_id>/characters')


@characters_bp.route('', methods=['GET'])
@jwt_required()
def list_characters(project_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        skip = request.args.get('skip', 0, type=int)
        limit = min(request.args.get('limit', 50, type=int), 50)
        characters = crud_character.list_characters(db.session, project_id, skip, limit)
        return jsonify([CharacterSchema.model_validate(c).model_dump() for c in characters]), 200
    except Exception as e:
        logger.error(f"Error listing characters: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@characters_bp.route('', methods=['POST'])
@jwt_required()
def create_character(project_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = CharacterCreate(**request.get_json())
        if data.race_id is not None:
            if not crud_character.validate_race_in_project(db.session, project_id, data.race_id):
                return jsonify({"error": "Race does not belong to this project"}), 400
        character = crud_character.create_character(db.session, project_id, data)
        logger.info("Character created", extra={'user_id': user.id, 'project_id': project_id, 'character_id': character.id})
        return jsonify(CharacterSchema.model_validate(character).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating character: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@characters_bp.route('/<int:character_id>', methods=['GET'])
@jwt_required()
def get_character(project_id: int, character_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        character = crud_character.get_character(db.session, project_id, character_id)
        if not character:
            return jsonify({"error": "Not found"}), 404
        return jsonify(CharacterSchema.model_validate(character).model_dump()), 200
    except Exception as e:
        logger.error(f"Error getting character: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@characters_bp.route('/<int:character_id>', methods=['PUT'])
@jwt_required()
def update_character(project_id: int, character_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = CharacterUpdate(**request.get_json())
        if data.race_id is not None:
            if not crud_character.validate_race_in_project(db.session, project_id, data.race_id):
                return jsonify({"error": "Race does not belong to this project"}), 400
        character = crud_character.update_character(db.session, project_id, character_id, data)
        if not character:
            return jsonify({"error": "Not found"}), 404
        return jsonify(CharacterSchema.model_validate(character).model_dump()), 200
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating character: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@characters_bp.route('/<int:character_id>', methods=['DELETE'])
@jwt_required()
def delete_character(project_id: int, character_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        if not crud_character.delete_character(db.session, project_id, character_id):
            return jsonify({"error": "Not found"}), 404
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting character: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
