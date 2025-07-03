import os
from pathlib import Path
import inquirer
import json
import pandas as pd

from siteplan_qualitycontrol.tasks import PARKING_MODULES, single_module_perform
from siteplan_qualitycontrol.utils import LogJson, global_var
from siteplan_qualitycontrol.analysis import zoning_post, parking_count_post
from siteplan_qualitycontrol.city_rules import zone_check, parking_requirement_call, contain_no_number
from siteplan_qualitycontrol.city_rules import string_to_formula, calculate_with_input
from siteplan_qualitycontrol.qc_basic import get_parking_requirement_info, get_parking_usage_info, analysis_condition_question
from siteplan_qualitycontrol.terminal_run import inquirer_list, inquirer_text
from siteplan_qualitycontrol.qc_basic import check_api_connection, get_chatbot_response


def parking(
        orig_img_path: str = None, 
        process_log: LogJson = None):
    # perform parking modules
    for module in PARKING_MODULES:
        single_module_perform(orig_img_path, module, process_log)

    # perform quality control
    # get the zoning information
    zoning_info = zoning_post(orig_img_path)
    # get the parking count information
    parking_count_info = parking_count_post(orig_img_path)

    # if any of these tasks failed, output the error message
    if zoning_info["status"] == "fail":
        error_message = zoning_info["error message"]
        print(error_message)
        return error_message
    else:
        city = zoning_info["city"]
        zone = zoning_info["zone"]

    if parking_count_info["status"] == "fail":
        error_message = parking_count_info["error message"]
        print(error_message)
        return error_message
    else:
        total_parking = parking_count_info["total_parking"]

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
    
    if tool_source == "Database (local)":
        # get the requirement from local database
        parking_requirement_df = parking_requirement_call(city, modified_zone)
        
        # get usage list and ask user to choose
        usage_type, usage_list = get_parking_usage_info(parking_requirement_df)
        usage = inquirer_list(
            "usage", 
            message=f"Choose {usage_type} of the project", 
            choices=usage_list)
        
        # get the requirement based on selected usage
        requirement, statement = get_parking_requirement_info(parking_requirement_df, usage)
        print(statement)
        # check if the statement is a legal formula
        if contain_no_number(statement):
            print("Not support.")
            return None
        
        # check if there is a condition statement
        # first level condition is marked using "[question] ? [state1] : [state2]"
        if statement.find(" ? ") != -1 and statement.find(" : ") != -1:
            # condition statement
            condition_str, choice_state = analysis_condition_question(statement, level=1)

            # ask user to choose between choices
            choice = inquirer_list(
                "choice", 
                message=condition_str, 
                choices=list(choice_state.keys()))
            
            # based on the choice, get the new statement
            statement = choice_state[choice]
            
            # for the new statement, check if it is a second level condition
            if statement.find(" ?? ") == -1:
                # there is no second level condition
                pass
            else: 
                condition_str, choice_state = analysis_condition_question(statement, level=2)

                # ask the user for the choice
                choice = inquirer_list(
                    "choice", 
                    message=condition_str, 
                    choices=list(choice_state.keys()))
                
                # based on the choice, get the new statement
                statement = choice_state[choice]
        
        # get list of required parameters from the statement
        p_list, statement = string_to_formula(statement)

        # user input for parameters
        param_val_dict = {}
        for p in p_list:
            val = inquirer_text(p, message=f"input {p}")
            param_val_dict[p] = val

        # calculate the minimum parking requirement
        minimum_parking_requirement = calculate_with_input(statement, param_val_dict)
        print(f"minimum parking requirement is {minimum_parking_requirement}.")

        # check if parking count meets the requirement
        if total_parking >= minimum_parking_requirement:
            print("Parking meets the requirement")
        else:
            print("Parking NOT meet the requirement")
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
                prompt=f"Does parking number {total_parking} satisfy the minimum parking requirement?")
            print(response)
            return None

