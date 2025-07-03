import uuid

from app.models import db, RegistrationCode


def create_registration_code():
    if RegistrationCode.query.filter_by(used=False).count() < 5:
        for i in range(5):
            new_code = RegistrationCode(code=str(uuid.uuid4()))
            db.session.add(new_code)
        db.session.commit()