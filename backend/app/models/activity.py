from app.models.database import db


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete="CASCADE"), nullable=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id', ondelete="CASCADE"), nullable=True)
    
    app = db.Column(db.String(120), nullable=True, unique=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    message = db.Column(db.String(), nullable=False, unique=False)
    type = db.Column(db.String(120), nullable=False, unique=False)


class ActivityServer(object):
    @staticmethod
    def add_user_activity(
        user_id: int = None,
        app: str = None, 
        message: str = None, 
        type: str = None):
        # no session id
        # no page id
        # app can be None
        new_activity = Activity(
            user_id = user_id, 
            app = app, 
            message = message, 
            type = type)
        db.session.add(new_activity)
        db.session.commit()

    @staticmethod
    def add_session_activity(
        user_id: int = None, 
        session_id: int = None, 
        app: str = None, 
        message: str = None, 
        type: str = None):
        # no page id
        # app can be None
        new_activity = Activity(
            user_id = user_id, 
            session_id = session_id, 
            app = app, 
            message = message, 
            type = type)
        db.session.add(new_activity)
        db.session.commit()
