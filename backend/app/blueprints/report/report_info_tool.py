import os
from pathlib import Path
import pandas as pd

from siteplan_qualitycontrol.utils import LogJson
from siteplan_qualitycontrol.tasks import KEY_MODULE_LIST
from siteplan_qualitycontrol.utils import ChatBotInputJson


def get_project_information(orig_img_path: str = None):
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    basic_info = {}
    # basic information
    if process_log.check("info-gen"):
        func = KEY_MODULE_LIST.get("info-gen").get("post")
        information = func(orig_img_path)
        basic_info["Project Title"] = information["title"]
        basic_info["Address / Location"] = information["address"]
        basic_info["Accessor Parcel Number(s)"] = ",".join(information["apn_list"])
    else:
        basic_info["Project Title"] = ""
        basic_info["Address / Location"] = ""
        basic_info["Accessor Parcel Number(s)"] = ""

    # zoning information
    if process_log.check("zoning"):
        func = KEY_MODULE_LIST.get("zoning").get("post")
        information = func(orig_img_path)
        if information["status"] == "succeed":
            basic_info["Zoning"] = information["zone"]
        else:
            basic_info["Zoning"] = ""
    else:
        basic_info["Zoning"] = ""

    # transfer information dict to table content data
    data = []
    for key in basic_info.keys():
        if type(basic_info[key]) == list:
            data.append([key, ",".join(basic_info[key])])
        else:
            data.append([key, basic_info[key]])

    return data

def get_dimension_control(
        orig_img_path: str = None, 
        current_page_folder: str = None):
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    # dimension control results
    if process_log.check("dimension-qc"):
        func = KEY_MODULE_LIST.get("dimension-qc").get("post")
        information = func(orig_img_path)
        if information["status"] == "succeed":
            image_path = os.path.join(Path(orig_img_path).parent, "image", "dimension_qc.png")
            information["image_path"] = image_path
            # create list data 
            information_list_data = [
                f"Total {information["total_check"]} dimension notations are checked.",
            ]
            results_list_data = [
                f"<font color=green>{information["correct"]}</font> pass.", 
                f"<font color=red>{information["total_check"] - information["correct"]} </font> not pass.",
            ]
            list_data = [
                f"Total {information["total_check"]} dimension notations are checked.", 
                f"<font color=green>{information["correct"]}</font> pass.", 
                f"<font color=red>{information["total_check"] - information["correct"]} </font> not pass.",
            ]
            return information_list_data, results_list_data, list_data, information
        
    return [], [], [], None

def get_parking_control(orig_img_path: str = None):
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    # parking count results
    if process_log.check("parking-count"):
        func = KEY_MODULE_LIST.get("parking-count").get("post")
        information = func(orig_img_path)
        if information["status"] == "succeed":
            image_path = os.path.join(Path(orig_img_path).parent, "image", "parking_count.png")
            information["image_path"] = image_path
            # create list data
            list_data = [
                f"Total {information["total_parking"]} parking spaces are proposed in the siteplan.",
            ]
            return list_data, information
    
    return [], None

def get_parking_cahtbot(orig_img_path: str = None):
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    # parking count results
    if process_log.check("parking-count"):
        chatbot_input_json = ChatBotInputJson(os.path.join(Path(orig_img_path).parent, "chatbot.json"))
        # get information for parking chatbot quality control
        information = chatbot_input_json.get_session("parking")
        if information is None:
            return [], None
        # create list data
        info_list_data = information["message"]
        result_list_data = [information["results"]]
        # generate information text
        info_text = f"Basic information \n {information["cal_prompt"].replace("\n", "<br />").split("Return calculated number")[0]}"
        answer_text = f"Required parking spaces check from ChatBot:\n {information["cal_answer"]}"
        answer_text = answer_text.replace("\n", "<br />")
        result_text = information["results"]
        requirement_text = f"Parking requirement reference information:\n {information["var_answer"].split("**Requirement:**")[1]}"
        requirement_text = requirement_text.replace("\n", "<br />")
        list_data = [
            info_text, 
            answer_text, 
            requirement_text
        ]
        return info_list_data, result_list_data, list_data, information
    
    return [], [], [], None



