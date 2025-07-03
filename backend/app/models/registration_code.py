import uuid

from app.models.database import db


class RegistrationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(120), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)


class RegistrationCodeServer(object):
    @staticmethod
    def set_code_used(code: str = None):
        code_to_update = RegistrationCode.query.filter_by(code=code).update({"used": True})
        db.session.commit()