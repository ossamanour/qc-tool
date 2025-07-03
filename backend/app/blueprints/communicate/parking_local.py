from flask import jsonify, session, request
import time

from app.models import User, Session, Page
from app.blueprints.communicate import communicate_bp
from siteplan_qualitycontrol.analysis import zoning_post, parking_count_post
from siteplan_qualitycontrol.city_rules import zone_check, parking_requirement_call, contain_no_number
from siteplan_qualitycontrol.city_rules import string_to_formula, calculate_with_input
from siteplan_qualitycontrol.qc_basic import get_parking_requirement_info, get_parking_usage_info, analysis_condition_question
from siteplan_qualitycontrol.terminal_run import inquirer_list, inquirer_text
from siteplan_qualitycontrol.qc_basic import check_api_connection, get_chatbot_response


# get the list of land use
@communicate_bp.route("/communicate/parking-landuse", methods=["POST"])
def parking_landuse():
    data = request.get_json()
    print(data)
    
    # get current user, project, and page
    # current_user = User.query.filter_by(email=session["current_user"]["email"]).first()
    # current_project = Project.query.filter_by(user_id=current_user.id, project_name=session["current_project"]["projectName"]).first()
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    # orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    orig_img_path = session["current_orig_img_path"]

    # get the zoning information
    zoning_info = zoning_post(orig_img_path)

    # if zoning failed, output the error message
    if zoning_info["status"] == "fail":
        response = {"status": "fail", 
                    "errorMessage": zoning_info["error message"]}
        return jsonify(response), 500
    else:
        city = zoning_info["city"]
        zone = zoning_info["zone"]

    # get the parking count information
    parking_count_info = parking_count_post(orig_img_path)

    # if parking count fail, putput the error message
    if parking_count_info["status"] == "fail":
        response = {"status": "fail", 
                    "errorMessage": parking_count_info["error message"]}
        return jsonify(response), 500
    else: 
        total_parking = parking_count_info["total_parking"]

    # modify the zone
    modified_zone_info = zone_check(zone, city)
    if modified_zone_info["status"] == "fail":
        response = {"status": "fail", 
                    "errorMessage": modified_zone_info["error message"]}
        return jsonify(response), 500
    else:
        modified_zone = modified_zone_info["zone"]

    print(modified_zone)

    # for either local database or chatbot, the user need to provide required information
    city = "Scottsdale"
    modified_zone = "(C-3)"
    print(f"{city} - {modified_zone}")

    # based on the city and zone, get the usage list
    parking_requirement_df = parking_requirement_call(city, modified_zone)
    session["parking_requirement_df"] = parking_requirement_df

    # get usage list and ask user to choose
    usage_type, usage_list = get_parking_usage_info(parking_requirement_df)

    response = {"usageType": usage_type, 
                "usageList": usage_list}
    return jsonify(response), 200


# get the usage and return the condition or not
@communicate_bp.route("/communicate/parking-condition1", methods=["POST"])
def parking_condition1():
    data = request.get_json()
    print(data)

    # parking_requirement_df = get_current_parking_requirement()
    parking_requirement_df = session["parking_requirement_df"]
    # get requirement base3d on selected usage
    selected_usage = data["selectedUsage"]
    requirement, statement = get_parking_requirement_info(parking_requirement_df, selected_usage)
    print(statement)
    # check if the statement is a legal formula
    if contain_no_number(statement):
        response = {"message": "fail", 
                    "error message": "not support"}
        return jsonify(response), 400

    # first level condition is marked using "[question] ? [state1] : [state2]"
    choice_state_return = []
    if statement.find(" ? ") != -1 and statement.find(" : ") != -1:
        # condition statement
        condition_str, choice_state = analysis_condition_question(statement, level=1)
        for key in choice_state.keys():
            choice_state_return.append({"key": key, "value": choice_state[key]})
        simple_statement = False
    else:
        # simple statement case
        condition_str = ""
        choice_state_return = []
        simple_statement = True
        # for simple statement, get the list of required parameter from the statement
        p_list, statement = string_to_formula(statement)

        # create list to return
        p_list_return = []
        for p in p_list:
            p_list_return.append({"name": p, "value": ""})

    response = {"message": "level 1", 
                "statement": statement,
                "simpleStatement": simple_statement, 
                "conditionStr": condition_str, 
                "choiceState": choice_state_return, 
                "paramList": p_list_return}
    return jsonify(response), 200


# get the second level condition if exist
@communicate_bp.route("/communicate/parking-condition2", methods=["POST"])
def parking_condition2():
    data = request.get_json()
    print(data)

    # return the condition choice of level 1
    selected_choice1 = data["selectedChoice"]
    choice_state1 = data["choiceState"]
    # based on the choice, get the new statement
    for state in choice_state1:
        if state["key"] == selected_choice1:
            statement = state["value"]
            break
    print(statement)

    # second level condition is marked using "[question] ?? [state1] :: [state2]"
    choice_state_return = []
    if statement.find(" ?? ") != -1 and statement.find(" :: ") != -1:
        # condition statement
        condition_str, choice_state = analysis_condition_question(statement, level=2)
        for key in choice_state.keys():
            choice_state_return.append({"key": key, "value": choice_state[key]})
        simple_statement = False
    else:
        # simple statement case
        condition_str = ""
        choice_state_return = []
        simple_statement = True
        # for simple statement, get the list of required parameter from the statement
        p_list, statement = string_to_formula(statement)

        # create list to return
        p_list_return = []
        for p in p_list:
            p_list_return.append({"name": p, "value": ""})

    response = {"message": "level 2", 
                "statement": statement,
                "simpleStatement": simple_statement, 
                "conditionStr": condition_str, 
                "choiceState": choice_state_return, 
                "paramList": p_list_return}
    return jsonify(response), 200

# get the final statement
@communicate_bp.route("/communicate/parking-paramlist", methods=["POST"])
def parking_paramlist():
    data = request.get_json()
    print(data)

    # return the condition choice of level 2
    selected_choice2 = data["selectedChoice"]
    choice_state2 = data["choiceState"]
    # based on the choice, get the new statement
    for state in choice_state2:
        if state["key"] == selected_choice2:
            statement = state["value"]
            break
    print(statement)

    # get list of required parameters from the statement
    p_list, statement = string_to_formula(statement)

    # create list to return
    p_list_return = []
    for p in p_list:
        p_list_return.append({"name": p, "value": ""})

    response = {"message": "param list", 
                "statement": statement, 
                "paramList": p_list_return}
    return jsonify(response), 200

# check results
@communicate_bp.route("/communicate/parking-check", methods=["POST"])
def parking_check():
    data = request.get_json()
    print(data)

    # get total parking count
    orig_img_path = session["current_orig_img_path"]
    # get the parking count information
    parking_count_info = parking_count_post(orig_img_path)
    total_parking = parking_count_info["total_parking"]

    statement = data["statement"]
    param_list = data["paramList"]
    chatbot_in_use = data["chatbotInUse"]

    param_val_dict = {}
    for param in param_list:
        param_val_dict[param["name"]] = param["value"]
    print(param_val_dict)

    # use chatbot or not
    if chatbot_in_use:
        # use chatbot
        results = "dummy"
    else:
        # calculate the minimum parking requirement
        minimum_parking_requirement = calculate_with_input(statement, param_val_dict)
        
        # check if parking count meets the requirement
        if total_parking >= minimum_parking_requirement:
            results = "Parking meets the requirement"
        else:
            results = "Parking NOT meet the requirement"

    response = {"message": "parking check", 
                "results": results}
    return jsonify(response), 200