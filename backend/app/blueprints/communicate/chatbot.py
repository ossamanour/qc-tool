import os
from pathlib import Path
from flask import jsonify, session, request
from flask import current_app

from app.models import db, User, Session, Page
from app.blueprints.communicate import communicate_bp
from siteplan_qualitycontrol.qc_basic import check_api_connection, get_chatbot_response
from siteplan_qualitycontrol.utils import global_var, LogJson
from siteplan_qualitycontrol.analysis import address_zoning_info_generate, apn_zoning_info_generate
from siteplan_qualitycontrol.city_rules import zone_list_call
from siteplan_qualitycontrol.analysis import zoning_post, information_post


# switch chatbot inuse status
@communicate_bp.route("/chatbot/switch", methods=["POST"])
def chatbot_switch():
    current_chatbot_stat = request.get_json()
    print(current_chatbot_stat)

    # chat status, if it's on, directly turn it off
    if current_chatbot_stat:
        response = {"status": True, 
                    "chatbotInUse": False}
        return jsonify(response)
    
    # if off, check chatbot availablity first
    message = check_api_connection()
    if message == "Connection Error":
        response = {"status": False, 
                    "errorMessage": "ChatBot not available."}
        return jsonify(response), 200

    response = {"status": True, 
                "chatbotInUse": True}
    return jsonify(response), 200

# chatbot basic info fetch
@communicate_bp.route("/chatbot/data-fetch", methods=["POST"])
def chatbot_data_fetch():
    # check if "currentApp" is in the session
    if "currentSession" in list(session.keys()):
        # check if the current app has the zoning task
        current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
        # from the current page, get the output folder for it
        orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")\
        # read in process log
        process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

        # check if zoning is done
        if process_log.check("zoning"):
            # call for post func
            # information_info = information_post(orig_img_path)
            zoning_info = zoning_post(orig_img_path)
            # print(information_info)
            print(zoning_info)
            # check if zoning succeed
            if (zoning_info["status"] == "succeed"):
                response = {"status": True, 
                            "existInfo": True, 
                            "city": zoning_info["city"],
                            "zone": zoning_info["zone"]}
        else:
            print("fail")
            # feed back list of available cities 
            city_list = global_var.SUPPORT_CITY
            response = {"status": True, 
                        "existInfo": False, 
                        "cityList": city_list}
    else:
        # feed back list of available cities 
        city_list = global_var.SUPPORT_CITY
        response = {"status": True, 
                    "existInfo": False,
                    "cityList": city_list}
    return jsonify(response), 200

# fetch zone
@communicate_bp.route("/chatbot/zone-fetch", methods=["POST"])
def chatbot_zone_fetch():
    data = request.get_json()
    city = data["city"]
    info_type = data["infoType"]
    address = data["address"]
    apn = data["apn"]
    print(data)

    if info_type == "ADDRESS":
        zoning_info = address_zoning_info_generate(address=address, city=city)
    else:
        zoning_info = apn_zoning_info_generate(apn=apn, city=city)

    if zoning_info["status"] == "fail":
        response = {"status": False, 
                    "errorMessage": zoning_info["error message"]}
    else:
        response = {"status": True, 
                    "source": info_type, 
                    "zone": zoning_info["zone"]}
    
    return jsonify(response), 200

# get zone list from given city
@communicate_bp.route("/chatbot/fetch-zone-list", methods=["POST"])
def fetch_zone_list():
    data = request.get_json()
    city = data.lower().capitalize()
    
    zone_codes = zone_list_call(city)
    zone_list = list(zone_codes.keys())
    print(zone_list)

    response = {"status": True, 
                "zoneList": zone_list}
    return jsonify(response), 200

# get response to the question
@communicate_bp.route("/chatbot/get-response", methods=["POST"])
def get_response():
    data = request.get_json()
    print(data)
    city = data["city"]
    zone = data["zone"]
    prompt = data["message"]
    use_tool = data["useTool"]

    # check if zone is empty
    if zone == "":
        response = {"status": False, 
                    "errorMessage": "No zone information"}
        return jsonify(response), 200

    # # check if chatbot is available
    # message = check_api_connection()
    # if message == "Connection Error":
    #     response = {"status": False, 
    #                 "errorMessage": "ChatBot not available."}
    #     return jsonify(response), 200

    # result = get_chatbot_response(zone=zone, 
    #                                prompt=prompt, 
    #                                use_tool=use_tool)

    result = "dummy result"

    # print(data)

    response = {"status": True, 
                "result": result}
    return jsonify(response), 200