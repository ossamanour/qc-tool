import os
from pathlib import Path
import shutil
from flask import jsonify
from flask import request, current_app, session

from app.models import db, User, Session, Page
from siteplan_qualitycontrol.utils import ProjectConfigJson
from app.blueprints.basic import basic_bp


# receive submitted tasks from fontend
@basic_bp.route("/task/submit", methods=["POST"])
def task_submit():
    data = request.get_json()
    print(data)

    # get current page
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from current page, get the output folder and the path to the original image
    session["current_orig_img_path"] = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    # check the config file
    session_folder = session["currentSession"]["session_folder"]
    config_file_path = os.path.join(current_app.config["SERVER_FOLDER"], session_folder, "input", "config.json")
    # if config file does not exist, send error message to front 
    if not os.path.exists(config_file_path):
        response = {"status": False, 
                    "errorMessage": "Config file not exist, please input config."}
        return jsonify(response), 200
    
    # check the config content based on different tasks
    print(session["currentApp"])
    # load config
    project_config = ProjectConfigJson(config_file_path)
    if session["currentApp"] == "costestimate":
        # for cost estimate, check if there is compnay and price sheet
        if (not project_config.check("company")) or (not project_config.check("price_sheet")):
            response = {"status": False, 
                        "errorMessage": "Missing configs"}
            return jsonify(response), 200

    if session["currentApp"] == "qualitycontrol":
        # if keynote task is submitted, a keynote_template config must exists
        if "KEYNOTE MATCH" in data["submittedTasks"]:
            print("in")
            if (not project_config.check("company")) or (not project_config.check("keynote_template")):
                response = {"status": False, 
                            "errorMessage": "Missing configs"}
                return jsonify(response), 200
        else:
            if not project_config.check("company"):
                response = {"status": False, 
                            "errorMessage": "Missing configs"}
                return jsonify(response), 200
            
    # this step is for quality-control only, to manage tasks for keynote and parking
    new_tasks = data["submittedTasks"]
    # add one more matching for keynote
    if "KEYNOTE MATCH" in data["submittedTasks"]:
        new_tasks.append("MATCHING")
    # add one more quality control for parking
    if "PARKING" in data["submittedTasks"]:
        new_tasks.append("PARKING QUALITY CONTROL")

    print("config ok")
    # for correct config file, copy it to the corresponding folder
    config_dst = os.path.join(current_app.config["SERVER_FOLDER"], Path(current_page.page_folder).parent, "config.json")
    shutil.copyfile(config_file_path, config_dst)

    response = {"status": True, 
                "todoTasks": new_tasks}
    return jsonify(response), 200