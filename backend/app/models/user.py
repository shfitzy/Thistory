from datetime import datetime
from app.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return f"<User {self.username}>"
