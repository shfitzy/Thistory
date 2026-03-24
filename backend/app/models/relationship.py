from datetime import datetime
from app.database import db


class EntityRelationship(db.Model):
    __tablename__ = "entity_relationships"

    id = db.Column(db.Integer, primary_key=True, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    from_entity_type = db.Column(db.String(50), nullable=False)  # location, race, character, event
    from_entity_id = db.Column(db.Integer, nullable=False)
    to_entity_type = db.Column(db.String(50), nullable=False)
    to_entity_id = db.Column(db.Integer, nullable=False)
    relationship_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __repr__(self):
        return f"<EntityRelationship {self.from_entity_type}:{self.from_entity_id} -> {self.to_entity_type}:{self.to_entity_id}>"
