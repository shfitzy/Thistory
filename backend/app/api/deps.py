from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def get_current_user():
    """Get the current authenticated user"""
    user_id = get_jwt_identity()
    if not user_id:
        return None
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    return user
