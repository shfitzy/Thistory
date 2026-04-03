from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import db
from app.crud import event as crud_event
from app.schemas.event import EventCreate, EventUpdate, Event as EventSchema
from app.api.deps import get_project_for_view, get_project_for_modify
import logging

logger = logging.getLogger("thistory")

events_bp = Blueprint('events', __name__, url_prefix='/api/v1/projects/<int:project_id>/events')


@events_bp.route('', methods=['GET'])
@jwt_required()
def list_events(project_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        skip = request.args.get('skip', 0, type=int)
        limit = min(request.args.get('limit', 50, type=int), 50)
        events = crud_event.list_events(db.session, project_id, skip, limit)
        return jsonify([EventSchema.model_validate(e).model_dump() for e in events]), 200
    except Exception as e:
        logger.error(f"Error listing events: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@events_bp.route('', methods=['POST'])
@jwt_required()
def create_event(project_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = EventCreate(**request.get_json())
        event = crud_event.create_event(db.session, project_id, data)
        logger.info("Event created", extra={'user_id': user.id, 'project_id': project_id, 'event_id': event.id})
        return jsonify(EventSchema.model_validate(event).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating event: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@events_bp.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(project_id: int, event_id: int):
    try:
        project, user, err = get_project_for_view(project_id)
        if err:
            return err
        event = crud_event.get_event(db.session, project_id, event_id)
        if not event:
            return jsonify({"error": "Not found"}), 404
        return jsonify(EventSchema.model_validate(event).model_dump()), 200
    except Exception as e:
        logger.error(f"Error getting event: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@events_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(project_id: int, event_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        data = EventUpdate(**request.get_json())
        event = crud_event.update_event(db.session, project_id, event_id, data)
        if not event:
            return jsonify({"error": "Not found"}), 404
        return jsonify(EventSchema.model_validate(event).model_dump()), 200
    except ValueError as e:
        return jsonify({"error": "Validation failed", "details": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating event: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@events_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(project_id: int, event_id: int):
    try:
        project, user, err = get_project_for_modify(project_id)
        if err:
            return err
        if not crud_event.delete_event(db.session, project_id, event_id):
            return jsonify({"error": "Not found"}), 404
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting event: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
