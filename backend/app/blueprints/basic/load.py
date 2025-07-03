from flask import jsonify
from flask import request, session

from app.models import User, Session
from app.blueprints.basic import basic_bp


# home page load
@basic_bp.route("/load/home", methods=["POST"])
def home_page_load():
    print("home page load")
    if "isAuthenticated" in session.keys() and session["isAuthenticated"]:
        # delete all keys except the auth-related ones
        auth_related_keys = ["_permanent", "isAuthenticated", "currentUser"]
        for key in list(session.keys()):
            if key not in auth_related_keys:
                session.pop(key, None)
        print(session)
        response = {"status": True, 
                    "isAuthenticated": session["isAuthenticated"], 
                    "username": session["currentUser"]["username"]}
    else:
        session.clear()
        home_related_keys = ["_permanent", "isAuthenticated"]
        for key in list(session.keys()):
            if key not in home_related_keys:
                session.pop(key, None)
        session["isAuthenticated"] = False
        print(session)
        response = {"status": True, 
                    "isAuthenticated": session["isAuthenticated"]}
    
    return jsonify(response), 200


@basic_bp.route("/load/dashboard", methods=["POST"])
def dashboard_page_load():
    print("dashboard page load")

    # for dashboard, detailed user information and session list information are send to frontend
    sessions = Session.query.filter_by(created_by=session["currentUser"]["id"], is_deleted=False).all()
    session_list = []
    for s in sessions:
        session_list.append({
            "sessionName": s.session_name, 
            "filename": s.filename, 
            "createdTime": s.created_time, 
            "modifiedTime": s.modified_time
        })

    # delete all keys except the auth-realted keys
    auth_related_keys = ["_permanent", "isAuthenticated", "currentUser"]
    for key in list(session.keys()):
        if key not in auth_related_keys:
            session.pop(key, None)
    print(session)

    response = {"status": True, 
                "isAuthenticated": session["isAuthenticated"], 
                "username": session["currentUser"]["username"], 
                "sessionList": session_list}
    return jsonify(response), 200


@basic_bp.route("/load/app", methods=["POST"])
def app_page_load():
    print("app page load")
    response = {"status": True, 
                "isAuthenticated": session["isAuthenticated"], 
                "username": session["currentUser"]["username"]}
    return jsonify(response), 200

@basic_bp.route("/load/initialize_app", methods=["POST"])
def initialize_app_load():
    print("initialize app loading")
    data = request.get_json()
    # set current app
    session["currentApp"] = data["currentApp"]
    response = {"status": True}
    print(session)
    return jsonify(response), 200


@basic_bp.route("/load/app_info", methods=["POST"])
def app_info_load():
    print("main app load")
    print(session)
    respose = {"status": True, 
               "currentSession": session["currentSession"], 
               "currentPage": session["currentPage"], 
               "currentDisplay": session["currentDisplay"]}

    return jsonify(respose), 200