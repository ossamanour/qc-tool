import os
from flask import jsonify
from flask import request, current_app, session
from werkzeug.utils import secure_filename
import datetime
import shutil

from app.models import db, User, Session, Page, SessionUserPermission, Activity
from app.models import ActivityServer
from app.blueprints.session import session_bp

from siteplan_qualitycontrol.basic import pdf_image_prepare


# create session (upload a file)
@session_bp.route("/session/create", methods=["POST"])
def create_session():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    if filename[-4:] != ".pdf":
        filename = filename + ".pdf"
    session_name = request.form["sessionName"]

    # check if session already exist
    current_user = User.query.filter_by(id=session["currentUser"]["id"]).first()
    if Session.query.filter_by(session_name=session_name, created_by=current_user.id, is_deleted=False).first():
        response = {"status": False, 
                    "errorMessage": "Session alrady exist. Please use a differnt name or load the existing session."}
        return jsonify(response), 200
    
    # create a session folder to save the file (have input and output sub-folders)
    session_folder = os.path.join(current_user.user_folder, session_name)
    abs_session_folder = os.path.join(current_app.config['SERVER_FOLDER'], session_folder)
    # check if already exist, name with a number
    if os.path.exists(abs_session_folder):
        i = 1
        while True:
            session_folder = os.path.join(current_user.user_folder, f"{session_name}_{i}")
            abs_session_folder = os.path.join(current_app.config["SERVER_FOLDER"], session_folder)
            if not os.path.exists(abs_session_folder):
                os.makedirs(abs_session_folder, exist_ok=True)
                os.makedirs(os.path.join(abs_session_folder, "input"), exist_ok=True)
                os.makedirs(os.path.join(abs_session_folder, "output"), exist_ok=True)
                break
            i = i + 1
    else:
        os.makedirs(abs_session_folder, exist_ok=True)
        os.makedirs(os.path.join(abs_session_folder, "input"), exist_ok=True)
        os.makedirs(os.path.join(abs_session_folder, "output"), exist_ok=True)

    # save the input pdf file 
    destination = os.path.join(abs_session_folder, "input", filename)
    file.save(destination)

    # deal with the input pdf file
    output_folder = os.path.join(abs_session_folder, "output")
    print("start")
    total_page = pdf_image_prepare(pdf_path=destination, 
                                   save_path=output_folder, 
                                   dpi=300)
    print("end")

    # add to session databse
    new_session = Session(created_by=current_user.id, 
                          session_name=session_name, 
                          filename=filename,
                          session_folder=session_folder, 
                          total_page=total_page)
    db.session.add(new_session)
    db.session.commit()

    # update session-user-permission table
    current_session = Session.query.filter_by(session_name=session_name, is_deleted=False).first()
    new_session_user = SessionUserPermission(user_id=current_user.id, 
                                             session_id=current_session.id, 
                                             role="admin")
    db.session.add(new_session_user)
    db.session.commit()
    
    # for each page, save in the database
    for i in range(total_page):
        page_number = i + 1
        page_folder = os.path.join(current_session.session_folder, "output", f"p{page_number}")
        new_page = Page(session_id=current_session.id,
                        page_number=page_number,
                        page_folder=page_folder)
        db.session.add(new_page)
        db.session.commit()

    # add activity
    ActivityServer.add_session_activity(user_id=current_user.id, 
                                        session_id=current_session.id, 
                                        message="session create", 
                                        type="session")

    # add session info to the cach session
    session["currentSession"] = {"id": current_session.id, 
                                 "session_name": current_session.session_name, 
                                 "filename": current_session.filename, 
                                 "session_folder": current_session.session_folder, 
                                 "total_page": current_session.total_page, 
                                 "config": current_session.config}

    # for initial display
    session["currentPage"] = 1
    current_page = Page.query.filter_by(session_id=current_session.id, page_number=session["currentPage"]).first()
    session["currentDisplay"] = os.path.join(current_page.page_folder, "original.png")
    
    print(session)
    response = {"status": True} 
    return jsonify(response), 200 


# delete session
@session_bp.route("/session/soft-delete", methods=["POST"])
def soft_delete_session():
    data = request.get_json()
    print(data)

    # instead of really delete it, we only mark it as deleted and keep the files on the server
    selected_session = Session.query.filter_by(created_by=session["currentUser"]["id"], session_name=data["sessionName"]).first()
    selected_session.set_deleted()
    
    # get the new session list
    sessions = Session.query.filter_by(created_by=session["currentUser"]["id"], is_deleted=False).all()
    session_list = []
    for s in sessions:
        session_list.append({
            "sessionName": s.session_name, 
            "filename": s.filename, 
            "createdTime": s.created_time, 
            "modifiedTime": s.modified_time
        })

    response = {"status": True, 
                "sessionList": session_list}
    return jsonify(response), 200


# load session
@session_bp.route("/session/load", methods=["POST"])
def load_session():
    data = request.get_json()
    print(data)

    # find the selected session
    current_user = User.query.filter_by(id=session["currentUser"]["id"]).first()
    current_session = Session.query.filter_by(created_by=session["currentUser"]["id"], session_name=data["sessionName"], is_deleted=False).first()
    
    # add activity
    ActivityServer.add_session_activity(user_id=current_user.id, 
                                        session_id=current_session.id, 
                                        message="session load", 
                                        type="session")

    # add session info to the cach session
    session["currentSession"] = {"id": current_session.id, 
                                 "session_name": current_session.session_name, 
                                 "filename": current_session.filename, 
                                 "session_folder": current_session.session_folder, 
                                 "total_page": current_session.total_page, 
                                 "config": current_session.config}

    # for initial display
    session["currentPage"] = 1
    print(session["currentSession"])
    current_page = Page.query.filter_by(session_id=current_session.id, page_number=session["currentPage"]).first()
    session["currentDisplay"] = os.path.join(current_page.page_folder, "original.png")
    
    print(session)

    response = {"status": True}
    return jsonify(response), 200