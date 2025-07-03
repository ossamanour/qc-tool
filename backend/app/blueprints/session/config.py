import os
from flask import jsonify
from flask import request, send_from_directory, current_app, session
from collections import OrderedDict
import shutil

from app.models import db, User, Session, Page
from app.blueprints.session import session_bp
from siteplan_qualitycontrol.company_config import COMPANY_FUNC_LISTS, list_all_company_template
from siteplan_qualitycontrol.ce_basic import list_all_price_sheet_templates, price_sheet_template_load
from siteplan_qualitycontrol.images import list_keynote_template, keynote_template_call
from siteplan_qualitycontrol.utils import ProjectConfigJson


# get the company template list
@session_bp.route("/config/company_list", methods=["POST"])
def company_template_list():
    print("config")
    current_session = Session.query.filter_by(id=session["currentSession"]["id"]).first()
    config = current_session.config
    print(config)

    if config is None or "company" not in config:
        temp_list = list_all_company_template()
        print(temp_list)

        # generate into array of dict
        template_list = []
        for template in temp_list:
            template_list.append({"value": template, 
                                  "label": template.upper()})
            
        response = {"status": True, 
                    "list": template_list}
    else:
        response = {"status": False, 
                    "company": config["company"]}
        
    return jsonify(response), 200

# get the company template
@session_bp.route("/config/template_path", methods=["POST"])
def company_template_path():
    data = request.get_json()
    print(data)

    company = data["value"]
    template_path_func = COMPANY_FUNC_LISTS.get(company).get("template_path")
    template_path = template_path_func()

    response = {"status": True, 
                "templatePath": template_path}
    return jsonify(response), 200

# view the template
@session_bp.route("/config/view_template/<path:filename>")
def view_company_template(filename):
    print(filename)
    if filename[0] == "/":
        filename = filename[1:]
    return send_from_directory("/", filename)

# get the list of keynote template
@session_bp.route("/config/keynote_list", methods=["POST"])
def keynote_template_list():
    print("config")
    current_session = Session.query.filter_by(id=session["currentSession"]["id"]).first()
    config = current_session.config

    if config is None or "keynote_template" not in config:
        template_list = list(list_keynote_template())
        print(template_list)
            
        response = {"status": True, 
                    "list": template_list}
    else:
        response = {"status": False, 
                    "keynoteTemplate": config["keynote_template"]}
        
    return jsonify(response), 200

# preview keynote
@session_bp.route("/config/keynote_view/<path:filename>")
def view_keynote_template(filename):
    print(filename)
    template_path, _ = keynote_template_call(filename)
    if template_path[0] == "/":
        template_path = template_path[1:]
    print(template_path)
    return send_from_directory("/", template_path)

# price sheet list
@session_bp.route("/config/pricesheet_list", methods=["POST"])
def pricesheet_list():
    print("config")
    current_session = Session.query.filter_by(id=session["currentSession"]["id"]).first()
    config = current_session.config

    if config is None or "price_sheet" not in config:
        temp_list = list_all_price_sheet_templates()
            
        template_list = []
        for template in temp_list:
            template_list.append({"value": template, 
                                  "label": template})
        print(template_list)
        response = {"status": True, 
                    "list": template_list}
    else:
        response = {"status": False, 
                    "price": config["price_sheet"]}
        
    return jsonify(response), 200


# preview price sheet template
@session_bp.route("/config/pricesheet_view", methods=["POST"])
def pricesheet_view():
    data = request.get_json()
    print(data)

    pricesheet_template_form = price_sheet_template_load(data["value"])
    onsite_df = pricesheet_template_form["onsite"]
    offsite_df = pricesheet_template_form["offsite"]
    onsite_df.fillna("", inplace=True)
    offsite_df.fillna("", inplace=True)

    response = {"status": True, 
                "sheetHeader": list(onsite_df), 
                "onsiteSheet": onsite_df.to_dict(orient="records", into=OrderedDict), 
                "offsiteSheet": offsite_df.to_dict(orient="records", into=OrderedDict)}
    return jsonify(response), 200

# generate config
@session_bp.route("/config/generate", methods=["POST"])
def generate_config():
    data = request.get_json()
    print(data)

    # find current session and current page
    session_folder = session["currentSession"]["session_folder"]
    config_path = os.path.join(current_app.config["SERVER_FOLDER"], session_folder, "input", "config.json")
    print(config_path)
    # create project config
    project_config = ProjectConfigJson(config_path=config_path)
    # for each config, check if already exist
    if "company" in data.keys():
        if not project_config.check("company"):
            project_config.update(key="company", value=data["company"])

    if "keynote" in data.keys():
        if not project_config.check("keynote_template"):
            project_config.update(key="keynote_template", value=data["keynote"])
    
    if "pricesheet" in data.keys():
        if not project_config.check("price_sheet"):
            project_config.update(key="price_sheet", value=data["pricesheet"])
    
    print(project_config.config_json)
    # update current session database
    current_session = Session.query.filter_by(id=session["currentSession"]["id"]).first()
    current_session.config = project_config.config_json
    db.session.commit()

    response = {"status": True}
    return jsonify(response), 200