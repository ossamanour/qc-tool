from werkzeug.security import generate_password_hash, check_password_hash

from app.models.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=False, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    user_folder = db.Column(db.String(120), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    registration_code = db.Column(db.String(120), unique=True, nullable=False)

    sessions = db.relationship("Session", backref="user", lazy=True, cascade="all, delete, delete-orphan")
    
    activity = db.relationship("Activity", backref="user", lazy=True, cascade="all, delete, delete-orphan")

    session_user_permission = db.relationship("SessionUserPermission", backref="user", lazy=True, cascade="all, delete, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)