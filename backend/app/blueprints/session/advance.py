import os
import json
from flask import jsonify
from flask import request, send_from_directory, current_app, session

from app.models import db, User, Session
from app.blueprints.session import session_bp
from siteplan_qualitycontrol.utils import AdvancedConfigJson


@session_bp.route("/advance/setup", methods=["POST"])
def advance_setup():
    data = request.get_json()
    print(data)

    ad_setting = {}
    for type in data.keys():
        sub_dict = {}
        for item in data[type]:
            sub_dict[item["title"]] = item["value"]
        ad_setting[type] = sub_dict
    print(ad_setting)

    # save to the input folder for current session
    session_folder = session["currentSession"]["session_folder"]
    advanced_path = os.path.join(current_app.config["SERVER_FOLDER"], session_folder, "input", "advance.json")
    # create config
    advanced_config = AdvancedConfigJson(advanced_path)
    advanced_config.update_dict(ad_setting)

    # update current session database
    current_session = Session.query.filter_by(id=session["currentSession"]["id"]).first()
    current_session.advanced = advanced_config.config_json
    db.session.commit()

    response = {"status": True}
    return jsonify(response), 200


# load the current config
@session_bp.route("/advance/load", methods=["POST"])
def advance_load():
    # save to the input folder for current session
    session_folder = session["currentSession"]["session_folder"]
    advanced_path = os.path.join(current_app.config["SERVER_FOLDER"], session_folder, "input", "advance.json")
    # create config
    advanced_config = AdvancedConfigJson(advanced_path)

    # create a format fits for the frontend
    config = advanced_config.config_json
    if not config:
        response = {"status": False}
    else:
        send_dict = {}
        for category in config.keys():
            send_dict[category] = []
            for key in config[category].keys():
                send_dict[category].append({
                    "title": key, 
                    "value": config[category][key]})
        response = {"status": True, 
                    "advancedConfig": send_dict}
        
    return jsonify(response), 200