"""
Functions of tools for building height quality control (local database).
"""
import os
import json


def single_param_analysis(
        single_requirement_dict: dict = None):
    """
    Function to analysis one parameter.

    @param: single_requirement_dict: dictionary of requirement for one parameter.

    @return: dictionary containing analysis results.
    """
    # input will be requirements for one parameter
    if len(single_requirement_dict) == 1 and list(single_requirement_dict.keys())[0] == "ALL":
        statement = single_requirement_dict["ALL"]
        maximum_height_limit = eval(statement)
        return {"status": "naive", 
                "maximum_height_limit": maximum_height_limit}

    choice_state = single_requirement_dict
    return {"status": "complicate", 
            "choice_state": choice_state}


def check_all_params(
        param_requirement_dict: dict = None):
    """
    Check all parameters to see if they meet the requirements.

    @param: param_requirement_dict: dictionary of all parameters needed to be checked.

    @return: final_check_result: boolean indicating if all parameters meet the requirement.
    @return: error_dict: dictionary containing all error messages if any parameter doesn't meet the requirement.
    """
    check_list = []
    error_dict = {}
    
    for key in param_requirement_dict.keys():
        proposed = float(param_requirement_dict[key]["val"])
        requirement = param_requirement_dict[key]["maximum_height_limit"]
        check_list.append(proposed <= requirement)
        if proposed > requirement:
            error_dict[key] = param_requirement_dict[key]
    final_check_result = all(check_list)
    return final_check_result, error_dict