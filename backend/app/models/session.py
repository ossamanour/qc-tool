from app.models.database import db


class Session(db.Model):
    # Session Table
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    session_name = db.Column(db.String(120), unique=False, nullable=False)
    filename = db.Column(db.String(120), unique=False, nullable=False)
    created_time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    modified_time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    session_folder = db.Column(db.String(120), unique=True, nullable=False)
    total_page = db.Column(db.Integer, nullable=False)
    config = db.Column(db.JSON, nullable=True)
    advanced = db.Column(db.JSON, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)

    pages = db.relationship("Page", backref="session", lazy=True, cascade="all, delete, delete-orphan")

    activity = db.relationship("Activity", backref="session", lazy=True, cascade="all, delete, delete-orphan")

    session_user_permission = db.relationship("SessionUserPermission", backref="session", lazy=True, cascade="all, delete, delete-orphan")

    def update_modified_time(self):
        self.modified_time = db.func.now()
        db.session.commit()

    def set_project_folder(self, project_folder):
        self.project_folder = project_folder
        db.session.commit()

    def set_deleted(self):
        self.is_deleted = True
        self.deleted_at = db.func.now()
        db.session.commit()