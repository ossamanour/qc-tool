import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base config"""
    # Database
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://siteplan_dev:siteplan_dev@192.168.1.222/siteplan_dev?application_name=dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # Security
    # SECRET_KEY = "110"
    # PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Server-end output folder
    BASEDIR = basedir
    SERVER_FOLDER = os.path.join(basedir, "server")
    UPLOAD_FOLDER = os.path.join(SERVER_FOLDER, "upload")

    # Session
    SESSION_TYPE = "filesystem"
    SECRET_KEY = "AAAAAAAaaaaaa!!!!!!"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_NAME = "my_session"

    # Running port information
    PORT = 8000


