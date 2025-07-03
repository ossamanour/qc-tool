import os
from pathlib import Path
from flask import jsonify, session, request
import time
import re

from app.models import User, Session, Page
from app.blueprints.communicate import communicate_bp
from app.blueprints.communicate.chatbot_utils import get_chatbot_response, get_chatbot_response_with_context
from siteplan_qualitycontrol.analysis import zoning_post, parking_count_post
from siteplan_qualitycontrol.city_rules import zone_check
from siteplan_qualitycontrol.utils import ChatBotInputJson


# receive landuse information
@communicate_bp.route("/communicate/parking-landuse", methods=["POST"])
def parking_landuse():
    data = request.get_json()
    landuse = data

    # get current user, project, and page
    # current_user = User.query.filter_by(email=session["current_user"]["email"]).first()
    # current_project = Project.query.filter_by(user_id=current_user.id, project_name=session["current_project"]["projectName"]).first()
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    # orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    orig_img_path = session["current_orig_img_path"]
    # load chatbot log 
    chatbot_input_json = ChatBotInputJson(os.path.join(Path(orig_img_path).parent, "chatbot.json"))

    # get the zoning information
    zoning_info = zoning_post(orig_img_path)

    # if zoning failed, output the error message
    if zoning_info["status"] == "fail":
        response = {"status": False, 
                    "errorMessage": zoning_info["error message"]}
        return jsonify(response), 500
    else:
        city = zoning_info["city"]
        zone = zoning_info["zone"]

    # modify the zone
    modified_zone_info = zone_check(zone, city)
    if modified_zone_info["status"] == "fail":
        response = {"status": False, 
                    "errorMessage": modified_zone_info["error message"]}
        return jsonify(response), 500
    else:
        modified_zone = modified_zone_info["zone"]
    print(f"{city} - {modified_zone}")

    # generate the prompt for chatbot to get required variables and conditions
    prompt = f"""
        Parking requirement for landuse of {landuse}.
        Return the required information (variables, condition choices if applicable) needed to calculate the required parking spaces, in the format: 
        **Variables:**
        [Variable1], [Variable2], [Variable3], ...
        **condition Choices:**
        [Condtion Choice1], [Condtion Choice2], [Condtion Choice3], ...
        **Requirement:** 
        [Requirement1], [Requirement2], ...
    """
    answer, context = get_chatbot_response(city, modified_zone, prompt)

    # generate variable list and condition list
    variable_list = answer.split("**Condition Choices:**")[0].split("**Variables:**")[1].split("\n")
    variable_list_return = [v for v in variable_list if v]
    condition_list = answer.split("**Condition Choices:**")[1].split("**Requirement:**")[0].split("\n")
    condition_list_return = [c for c in condition_list if c]

    # save information
    chatbot_input_json.update_info("parking", "landuse", landuse)
    chatbot_input_json.update_info("parking", "var_prompt", prompt)
    chatbot_input_json.update_info("parking", "var_answer", answer)
    chatbot_input_json.update_info("parking", "context", context)

    response = {"status": True, 
                "variableList": variable_list_return, 
                "conditionList": condition_list_return}
    return jsonify(response), 200

# received input information
@communicate_bp.route("/communicate/parking-check", methods=["POST"])
def parking_check():
    data = request.get_json()
    print(data)
    landuse = data["landuse"]
    variable_dict = data["variableDict"]
    condition_dict = data["conditionDict"]

    # get current user, project, and page
    # current_user = User.query.filter_by(email=session["current_user"]["email"]).first()
    # current_project = Project.query.filter_by(user_id=current_user.id, project_name=session["current_project"]["projectName"]).first()
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    # orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    orig_img_path = session["current_orig_img_path"]
    # load chatbot log 
    chatbot_input_json = ChatBotInputJson(os.path.join(Path(orig_img_path).parent, "chatbot.json"))

    # create prompt
    prompt = f"Parking requirement for landuse of {landuse}."
    # add variables
    prompt = prompt + "\n**Variables:**"
    for key in variable_dict.keys():
        prompt = prompt + f"\n{key} = {variable_dict[key]}"
    # add conditions
    prompt = prompt + "\n**Condition Choices:**"
    for key in condition_dict.keys():
        prompt = prompt + f"\n{key} = {condition_dict[key]}"
    # add return request
    prompt = prompt + """
    Return calculated the minimum parking spaces in the format:
    [ANS] [number of spaces]
    """
    
    # get context
    context = chatbot_input_json.get("parking", "context")

    answer = get_chatbot_response_with_context(prompt, context)

    # save results to chatbot info
    chatbot_input_json.update_info("parking", "cal_prompt", prompt)
    chatbot_input_json.update_info("parking", "cal_answer", answer)

    # get the final number of requirement
    number_string = re.findall(r'\d+', answer.split("[ANS]")[1])[0]
    if number_string == "":
        required_parking = 0
    else:
        required_parking = eval(number_string)
    chatbot_input_json.update_info("parking", "required", required_parking)
    print(required_parking)

    # get the parking count information
    parking_count_info = parking_count_post(orig_img_path)

    # if parking count fail, putput the error message
    if parking_count_info["status"] == "fail":
        response = {"status": True, 
                    "totalParking": parking_count_info["error message"], 
                    "requiredParking": required_parking, 
                    "message": "not appilcable"}
        chatbot_input_json.update_info("parking", "results", "no proposed parking information.")
        return jsonify(response), 500
    else: 
        total_parking = parking_count_info["total_parking"]

    message = []
    # add information of landuse
    message.append(f"Landuse is {landuse}.")
    # add variables
    for key in variable_dict.keys():
        if variable_dict[key] != "":
            message.append(f"{key} = {variable_dict[key]}")
    for key in condition_dict.keys():
        if condition_dict[key] != "":
            message.append(f"{key} = {condition_dict[key]}")
    chatbot_input_json.update_info("parking", "message", message)

    if total_parking >= required_parking:
        results = "Proposed parking satisfied the city requirement."
    else:
        results = "Proposed parking does not satisfy the city requirement."
    chatbot_input_json.update_info("parking", "results", results)
    # add results
    message.append(results)

    response = {"status": True, 
                "totalParking": total_parking, 
                "requiredParking": required_parking, 
                "message": message}
    return jsonify(response), 200
