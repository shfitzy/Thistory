from typing import Optional, List
from app.database import db
from app.models.user import User
from app.core.security import get_password_hash


def get_user(user_id: int) -> Optional[User]:
    """Get a user by ID"""
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email: str) -> Optional[User]:
    """Get a user by email"""
    return User.query.filter_by(email=email).first()


def get_user_by_username(username: str) -> Optional[User]:
    """Get a user by username"""
    return User.query.filter_by(username=username).first()


def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    """Get a list of users"""
    return User.query.offset(skip).limit(limit).all()


def create_user(user_data: dict) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user_data.get("password"))
    db_user = User(
        email=user_data.get("email"),
        username=user_data.get("username"),
        hashed_password=hashed_password,
    )
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user


def update_user(user_id: int, user_data: dict) -> Optional[User]:
    """Update a user"""
    db_user = get_user(user_id)
    if not db_user:
        return None
    
    # Update fields if provided
    if "email" in user_data and user_data["email"] is not None:
        db_user.email = user_data["email"]
    if "username" in user_data and user_data["username"] is not None:
        db_user.username = user_data["username"]
    if "password" in user_data and user_data["password"] is not None:
        db_user.hashed_password = get_password_hash(user_data["password"])
    
    db.session.commit()
    db.session.refresh(db_user)
    return db_user


def delete_user(user_id: int) -> bool:
    """Delete a user"""
    db_user = get_user(user_id)
    if not db_user:
        return False
    
    db.session.delete(db_user)
    db.session.commit()
    return True
