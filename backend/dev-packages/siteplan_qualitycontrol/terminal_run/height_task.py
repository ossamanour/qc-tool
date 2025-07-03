import os
from pathlib import Path

from siteplan_qualitycontrol.utils import LogJson
from siteplan_qualitycontrol.analysis import zoning_post
from siteplan_qualitycontrol.city_rules import zone_check, height_requirement_call
from siteplan_qualitycontrol.city_rules import string_to_formula, calculate_with_input
from siteplan_qualitycontrol.terminal_run import inquirer_list, inquirer_text
from siteplan_qualitycontrol.qc_basic import check_api_connection, get_chatbot_response
from siteplan_qualitycontrol.qc_basic import single_param_analysis, check_all_params


def height(
        orig_img_path: str = None, 
        process_log: LogJson = None):
    # at this time, there is no building height information detected from siteplan    
    
    # perform quality control
    # get the zoning information
    zoning_info = zoning_post(orig_img_path)

    # if zoning failed, output the error message
    if zoning_info["status"] == "fail":
        error_message = zoning_info["error message"]
        print(error_message)
        return error_message
    else:
        city = zoning_info["city"]
        zone = zoning_info["zone"]

    # modify the zone
    modified_zone_info = zone_check(zone, city)
    if modified_zone_info["status"] == "fail":
        error_message = modified_zone_info["error message"]
        print(error_message)
        return error_message
    else:
        modified_zone = modified_zone_info["zone"]

    # ask the user to choose between local database and chatbot
    tool_source = inquirer_list(
        "tool_source", 
        message="Choose source to do quality control", 
        choices=["ChatBot", "Database (local)"])
    print(f"Perform quality control based on {tool_source}")

    city = "Scottsdale"
    modified_zone = "(R-3)"
    print(f"{city} - {modified_zone}")

    if tool_source == "Database (local)":
        # based on the city and zone, get the corresponding height requirement
        height_requirement_dict = height_requirement_call(city, modified_zone)

        # get all required params (keys) in the building height requirement
        param_requirement_dict = {}
        for key in height_requirement_dict.keys():
            print(key)
            # analysis the requirement
            single_param_info = single_param_analysis(height_requirement_dict[key])

            if single_param_info["status"] == "naive":
                # for this key param, one simple requirement is set for "ALL"
                maximum_height_limit = single_param_info["maximum_height_limit"]
            else:
                # for cases with different conditions
                choice_state = single_param_info["choice_state"]
                
                # ask user to choose
                choice = inquirer_list(
                    "choice", 
                    message="Choose the one that match", 
                    choices=list(choice_state.keys()))
                
                # based on the choice, get the statement
                statement = choice_state[choice]

                # get list of required parameters from the statement
                p_list, statement = string_to_formula(statement)

                # deal with different cases
                if len(p_list) != 0:
                    # list not empty
                    param_val = {}
                    for p in p_list:
                        val = inquirer_text(p, message=f"input {p}")
                        param_val[p] = val
                    maximum_height_limit = calculate_with_input(statement, param_val)
                elif statement is not None:
                    # pure number case
                    maximum_height_limit = eval(statement)
                else:
                    maximum_height_limit = None
                
                # for cases maximum_height_list is not none, ask input
                if maximum_height_limit != None:
                    param_val = inquirer_text(key, message=f"input {key}")
                    # save to the dict
                    param_requirement_dict[key] = {"val": param_val, 
                                                   "maximum_height_limit": maximum_height_limit}
        # check if all param meets the requirement
        check_result, error_dict = check_all_params(param_requirement_dict)

        if check_result:
            print("Building height meets the requirements.")
        else:
            print("Building height does not meets the requirement, please review.")
            for key in error_dict.keys():
                print(f"The maximum {key} required is {error_dict[key]["val"]}, but the current site plan has {key} of {error_dict[key]["maximum_height_limit"]}.")

    else:
        # for chatbot
        # check if chatbot is available
        message = check_api_connection()
        if message == "Connection Error":
            print(message)
            return None
        else:
            response = get_chatbot_response(
                modified_zone, 
                prompt=f"What is the building height requirement?")
            print(response)
            return None