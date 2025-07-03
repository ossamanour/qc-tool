import os
from flask import jsonify
from flask import request, current_app, session
from flask_session import Session
from werkzeug.utils import secure_filename

from app.models import db, RegistrationCode, User, Activity
from app.models import RegistrationCodeServer, ActivityServer
from app.blueprints.basic import basic_bp


# register 
@basic_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    password = data["password"]
    registration_code = data["registrationCode"]

    # check if user already exist
    if User.query.filter_by(email=email).first():
        response = {"status": False, 
                    "errorMessage": "Email exist, log in or try a different email."}
        return jsonify(response), 200
    
    # check if the registration code is available
    if not RegistrationCode.query.filter_by(code=registration_code, used=False).first():
        response = {"status": False, 
                    "errorMessage": "Invalid registration code."}
        return jsonify(response), 200
    
    # with valid registration code and new user, start register
    # create folder on server for new user
    user_folder = secure_filename(email).replace('.', '-')
    os.makedirs(os.path.join(current_app.config["SERVER_FOLDER"], user_folder), exist_ok=True)

    new_user = User(email=email, 
                    username=username, 
                    user_folder=user_folder, 
                    registration_code=registration_code)
    new_user.set_password(password=password)
    db.session.add(new_user)
    db.session.commit()

    # set the used registration code
    RegistrationCodeServer.set_code_used(code=registration_code)

    # add information in session
    # automatically log in after register successfully
    current_user = User.query.filter_by(email=email).first()
    session["currentUser"] = {"id": current_user.id, 
                              "email": current_user.email, 
                              "username": current_user.username, 
                              "user_folder": current_user.user_folder}
    session["isAuthenticated"] = True

    # add activity
    ActivityServer.add_user_activity(user_id=current_user.id, 
                                     message="user register", 
                                     type="auth")

    response = {"status": True, 
                "isAuthenticated": True, 
                "username": current_user.username}
    return jsonify(response), 201

# login
@basic_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session["currentUser"] = {"id": user.id, 
                                  "email": user.email, 
                                  "username": user.username, 
                                  "user_folder": user.user_folder}
        session["isAuthenticated"] = True
        # add activity
        ActivityServer.add_user_activity(user_id=user.id, 
                                         message="user log in", 
                                         type="auth")
        
        response = {"status": True, 
                    "isAuthenticated": True, 
                    "username": user.username}
    else:
        response = {"status": False, 
                    "errorMessage": "Invalid email or password."}

    return jsonify(response), 200

# logout
@basic_bp.route("/auth/logout", methods=["POST"])
def logout():
    ActivityServer.add_user_activity(user_id=session["currentUser"]["id"], 
                                     message="user log out", 
                                     type="auth")
    session.clear()
    session["isAuthenticated"] = False
    response = {"status": True, 
                "isAuthenticated": session["isAuthenticated"]}
    return jsonify(response), 200
