from app.models.database import db


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete="CASCADE"), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    page_folder = db.Column(db.String(120), unique=True, nullable=False)
    tasks = db.Column(db.JSON, nullable=True)

    activity = db.relationship("Activity", backref="page", lazy=True, cascade="all, delete, delete-orphan")


