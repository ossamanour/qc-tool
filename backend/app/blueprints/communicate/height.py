from flask import jsonify, session, request
import time

from app.models import User, Session, Page
from app.blueprints.communicate import communicate_bp
from siteplan_qualitycontrol.analysis import zoning_post
from siteplan_qualitycontrol.city_rules import zone_check, height_requirement_call
from siteplan_qualitycontrol.city_rules import string_to_formula, calculate_with_input
from siteplan_qualitycontrol.terminal_run import inquirer_list, inquirer_text
from siteplan_qualitycontrol.qc_basic import check_api_connection, get_chatbot_response
from siteplan_qualitycontrol.qc_basic import single_param_analysis, check_all_params



# building height quality control 
@communicate_bp.route("/communicate/height-param-gen", methods=["POST"])
def height_param_gen():
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
    modified_zone = "(R-3)"
    print(f"{city} - {modified_zone}")

    # based on the city and zone, get the corresponding height requirement
    height_requirement_dict = height_requirement_call(city, modified_zone)

    # get all required params (keys) in the building height requirement
    param_requirement_dict = {}
    param_requirement_list = []
    for key in height_requirement_dict.keys():
        # analysis the requirement
        single_param_info = single_param_analysis(height_requirement_dict[key])

        if single_param_info["status"] == "naive":
            # for this key param, one simple requirement is set for "ALL"
            maximum_height_limit = single_param_info["maximum_height_limit"]
            choice_state = {}
            choices = []

        else: 
            # for cases with different conditions
            choice_state = single_param_info["choice_state"]
            choices = list(choice_state.keys())
            maximum_height_limit = None
        
        param_requirement_list.append({"key": key, 
                                       "choiceState": choice_state, 
                                       "choices": choices, 
                                       "maximumHeightLimit": maximum_height_limit})

    print(param_requirement_list)
    session["param_requirement_list"] = param_requirement_list

    response = {"message": "height", 
                "paramRequirementList": param_requirement_list}
    return jsonify(response), 200


# received the selected condition and send back the required param list
@communicate_bp.route("/communicate/height-condition", methods=["POST"])
def height_condition():
    data = request.get_json()
    print(data)

    # return the required p_list
    p_list, statement = string_to_formula(data["statement"])
    # create a p_list to store p name and value
    print(statement)
    if statement is None:
        print("aa")
        statement = ""
    param_val = []
    for p in p_list:
        param_val.append({"name": p, "value": 0})

    response = {"message": "condition", 
                "paramList": param_val, 
                "statement": statement}
    return jsonify(response), 200


# check the results
@communicate_bp.route("/communicate/height-check", methods=["POST"])
def height_check():
    data = request.get_json()
    # print(data)

    # create param_requirement_dict
    param_requirement_dict = {}
    for param in data:
        p_list = param["paramList"]
        statement = param["statement"]
        print(statement)
        if len(p_list) != 0:
            param_val = {}
            for p in param["paramList"]:
                param_val[p["name"]] = p["value"]
            maximum_height_limit = calculate_with_input(statement, param_val)
        elif statement != "":
            # pure number
            maximum_height_limit = eval(statement)
        else:
            maximum_height_limit = None

        if maximum_height_limit != None:
            param_requirement_dict[param["key"]] = {"val": param["value"], 
                                                 "maximum_height_limit": maximum_height_limit}
    print(param_requirement_dict)

    check_result, error_dict = check_all_params(param_requirement_dict)

    if check_result:
        return_message = "Building height meets the requirements."
    else:
        return_message = "Building height does not meets the requirement, please review."
        for key in error_dict.keys():
            return_message = return_message + f" The maximum {key} required is {error_dict[key]["maximum_height_limit"]}, but the current site plan has {key} of {error_dict[key]["val"]}."

    response = {"message": "height check", 
                "checkResult": check_result, 
                "return_message": return_message}
    return jsonify(response), 200