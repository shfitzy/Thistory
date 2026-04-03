from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import db
from app.crud import location as crud_location
from app.schemas.location import LocationCreate, LocationUpdate, Location as LocationSchema
from app.api.deps import get_project_for_view, get_project_for_modify
import logging

logger = logging.getLogger("thistory")

locations_bp = Blueprint('locations', __name__, url_prefix='/api/v1/projects/<int:project_id>/locations')


@locations_bp.route('', methods=['GET'])
@jwt_required()
def list_locations(project_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        skip = request.args.get('skip', 0, type=int)
        limit = min(request.args.get('limit', 50, type=int), 50)
        locations = crud_location.list_locations(db.session, project_id, skip, limit)
        return jsonify([LocationSchema.model_validate(l).model_dump() for l in locations]), 200
    except Exception as e:
        logger.error(f"Error listing locations: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@locations_bp.route('', methods=['POST'])
@jwt_required()
def create_location(project_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = LocationCreate(**request.get_json())
        location = crud_location.create_location(db.session, project_id, data)
        logger.info("Location created", extra={'user_id': user.id, 'project_id': project_id, 'location_id': location.id})
        return jsonify(LocationSchema.model_validate(location).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating location: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@locations_bp.route('/<int:location_id>', methods=['GET'])
@jwt_required()
def get_location(project_id: int, location_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        location = crud_location.get_location(db.session, project_id, location_id)
        if not location:
            return jsonify({"error": "Not found"}), 404
        return jsonify(LocationSchema.model_validate(location).model_dump()), 200
    except Exception as e:
        logger.error(f"Error getting location: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@locations_bp.route('/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(project_id: int, location_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = LocationUpdate(**request.get_json())
        location = crud_location.update_location(db.session, project_id, location_id, data)
        if not location:
            return jsonify({"error": "Not found"}), 404
        return jsonify(LocationSchema.model_validate(location).model_dump()), 200
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating location: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@locations_bp.route('/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(project_id: int, location_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        if not crud_location.delete_location(db.session, project_id, location_id):
            return jsonify({"error": "Not found"}), 404
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting location: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
