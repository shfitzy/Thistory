from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import db
from app.crud import race as crud_race
from app.schemas.race import RaceCreate, RaceUpdate, Race as RaceSchema
from app.api.deps import get_project_for_view, get_project_for_modify
import logging

logger = logging.getLogger("thistory")

races_bp = Blueprint('races', __name__, url_prefix='/api/v1/projects/<int:project_id>/races')


@races_bp.route('', methods=['GET'])
@jwt_required()
def list_races(project_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        skip = request.args.get('skip', 0, type=int)
        limit = min(request.args.get('limit', 50, type=int), 50)
        races = crud_race.list_races(db.session, project_id, skip, limit)
        return jsonify([RaceSchema.model_validate(r).model_dump() for r in races]), 200
    except Exception as e:
        logger.error(f"Error listing races: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@races_bp.route('', methods=['POST'])
@jwt_required()
def create_race(project_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = RaceCreate(**request.get_json())
        race = crud_race.create_race(db.session, project_id, data)
        logger.info("Race created", extra={'user_id': user.id, 'project_id': project_id, 'race_id': race.id})
        return jsonify(RaceSchema.model_validate(race).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating race: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@races_bp.route('/<int:race_id>', methods=['GET'])
@jwt_required()
def get_race(project_id: int, race_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        race = crud_race.get_race(db.session, project_id, race_id)
        if not race:
            return jsonify({"error": "Not found"}), 404
        return jsonify(RaceSchema.model_validate(race).model_dump()), 200
    except Exception as e:
        logger.error(f"Error getting race: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@races_bp.route('/<int:race_id>', methods=['PUT'])
@jwt_required()
def update_race(project_id: int, race_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = RaceUpdate(**request.get_json())
        race = crud_race.update_race(db.session, project_id, race_id, data)
        if not race:
            return jsonify({"error": "Not found"}), 404
        return jsonify(RaceSchema.model_validate(race).model_dump()), 200
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating race: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@races_bp.route('/<int:race_id>', methods=['DELETE'])
@jwt_required()
def delete_race(project_id: int, race_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        if not crud_race.delete_race(db.session, project_id, race_id):
            return jsonify({"error": "Not found"}), 404
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting race: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
