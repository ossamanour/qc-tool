import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
import sys
sys.path.append("./dev-packages")
print(sys.path)

from siteplan_qualitycontrol import global_var
print(global_var.SUPPORT_CITY)

from .models import db
from .models import create_registration_code

from .blueprints.basic import basic_bp
from .blueprints.session import session_bp
from .blueprints.communicate import communicate_bp
from .blueprints.report import report_bp
from .blueprints.module import module_bp

def create_app():
    # create app instance
    app = Flask(__name__)
    # make backend connected to frontend
    cors = CORS(app, origins="*", expose_headers="Authorization", supports_credentials=True)
    # load config
    app.config.from_object("config.Config")    
    print(app.config["SERVER_FOLDER"])

    # app.secret_key = os.urandom(14)
    app.secret_key = "AAAAAAAaaaaaa!!!!!!"

    # create database for the app
    db.init_app(app)
    migrate = Migrate(app, db)

    # initialize session
    Session(app)

    # create registration code if available code is less than 5
    with app.app_context():
        create_registration_code()

    # register blueprints
    app.register_blueprint(basic_bp, url_prefix="/api")
    app.register_blueprint(session_bp, url_prefix="/api")
    app.register_blueprint(communicate_bp, url_prefix="/api")
    app.register_blueprint(report_bp, url_prefix="/api")
    app.register_blueprint(module_bp, url_prefix="/api")

    return app
