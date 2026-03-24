from datetime import datetime
from app.database import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(500), nullable=False)
    long_description = db.Column(db.Text, nullable=False)
    visibility = db.Column(db.String(10), default="private", nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    # Relationships
    owner = db.relationship("User", back_populates="projects")
    locations = db.relationship("Location", back_populates="project", cascade="all, delete-orphan")
    races = db.relationship("Race", back_populates="project", cascade="all, delete-orphan")
    characters = db.relationship("Character", back_populates="project", cascade="all, delete-orphan")
    events = db.relationship("Event", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.title}>"
