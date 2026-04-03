from app.database import db


class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="unknown")  # living, deceased, unknown
    age = db.Column(db.Integer, nullable=True)
    race_id = db.Column(db.Integer, db.ForeignKey("races.id", ondelete="SET NULL"), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    project = db.relationship("Project", back_populates="characters")
    race = db.relationship("Race", back_populates="characters")

    def __repr__(self):
        return f"<Character {self.name}>"
