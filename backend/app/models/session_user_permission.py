from app.models.database import db


class SessionUserPermission(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete="CASCADE"), primary_key=True, nullable=False)

    role = db.Column(db.String(120), unique=False, nullable=False)
