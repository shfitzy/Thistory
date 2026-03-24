from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request
from flask_jwt_extended import get_jwt_identity


def get_user_id_for_rate_limit():
    """Get user ID from JWT for rate limiting, fallback to IP"""
    try:
        user_id = get_jwt_identity()
        return str(user_id) if user_id else get_remote_address()
    except:
        return get_remote_address()


def create_limiter(app):
    """Create and configure Flask-Limiter"""
    limiter = Limiter(
        app=app,
        key_func=get_user_id_for_rate_limit,
        default_limits=["100 per minute"],
        storage_uri="memory://",
        strategy="fixed-window"
    )
    return limiter
