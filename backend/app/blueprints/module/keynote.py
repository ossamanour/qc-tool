import os
from flask import jsonify, request, session, current_app
import time
import json

from app.models import db, Session, User, Page
from app.blueprints.module import module_bp
from app.blueprints.module.utils import simple_module_perform, simple_module_post
from siteplan_qualitycontrol.analysis import keynote_generate_post, keynote_match_pre
from siteplan_qualitycontrol.analysis import keynote_match, keynote_match_post


# generate keynotes
@module_bp.route("/module/keynote-gen", methods=["POST"])
def keynote_gen():
    module_name = "keynote-gen"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    print(return_response)
    # time.sleep(5)

    message = []
    if return_response["status"] == "succeed":
        # message.append(f"Totally {return_response["total_keynotes"]} keynotes detected.")

        current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
        session["currentDisplay"] = os.path.join(current_page.page_folder, "image", "keynote_pair.png")
    else:
        message.append("No keynotes detected.")

    response = {"status": True, 
                "message": message, 
                "currentDisplay": session["currentDisplay"]}

    return jsonify(response), 200


# prepare for keynote match
@module_bp.route("/module/keynote-match-prepare", methods=["POST"])
def keynote_match_prepare():
    orig_img_path = session["current_orig_img_path"]

    # get the keynote generation information
    keynote_generate_info = keynote_generate_post(orig_img_path)
    if keynote_generate_info["status"] == "fail":
        response = {"message": ["No keynote detected"]}
    else:
        # do prepare for the keynote matching
        keynote_match_pre(orig_img_path)
        keynote_num = keynote_generate_info["total_keynotes"]
        response = {"message": [f"{keynote_num} keynotes detected, start matching."], 
                    "keynoteNum": keynote_num}
    return jsonify(response), 200


# perform keynote matching based on index
@module_bp.route("/module/keynote-match/<int:index>", methods=["POST"])
def keynote_match_single(index):
    print(index)
    orig_img_path = session["current_orig_img_path"]

    # check if match has done
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    keynote_match_file_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "data", "keynote_match.json")
    if not os.path.exists(keynote_match_file_path):
        # perform keynote match for keynote #index
        keynote_match(orig_img_path, index)
    else:
        with open(keynote_match_file_path, "r") as fp:
            keynote_match_info = json.load(fp)

        if f"keynote-{index+1}" not in keynote_match_info.keys():
            # perform keynote match for keynote #index
            keynote_match(orig_img_path, index)
        else:
            time.sleep(3)

    # do post
    # keynote_match_info = keynote_match_post(orig_img_path, index)
    with open(keynote_match_file_path, "r") as fp:
            keynote_match_info = json.load(fp)

    message = []
    sub_keynote_match_info = keynote_match_info[f"keynote-{index+1}"]
    if sub_keynote_match_info["status"] == "succeed":
        message.append(f"Keynote {index+1}: {sub_keynote_match_info["match-number"]} matches are found.")
    else:
        message.append(f"Keynote {index+1}: No match found.")

    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    session["currentDisplay"] = os.path.join(current_page.page_folder, "image", "keynote_match", f"keynote-{index+1}.png")

    response = {"status": True, 
                "message": message, 
                "matchInfo": keynote_match_info, 
                "currentDisplay": session["currentDisplay"]}
    return jsonify(response), 200


