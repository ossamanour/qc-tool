import os
from flask import jsonify, session
import time

from app.models import db, Session, User, Page
from app.blueprints.module import module_bp
from app.blueprints.module.utils import simple_module_perform, simple_module_post

# scale-gen
@module_bp.route("/module/scale-gen", methods=["POST"])
def scale_gen():
    module_name = "scale-gen"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    print(return_response)
    # time.sleep(5)

    message = []
    message.append(f"""SCALE: 1" = {return_response["scale_number"]}'""")

    response ={"status": True, 
               "message": message}

    # response = {"message": module_name}
    return jsonify(response), 200

# arrow-gen
@module_bp.route("/module/arrow-gen", methods=["POST"])
def arrow_gen():
    module_name = "arrow-gen"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    response = simple_module_post(module_name)
    print(response)
    # time.sleep(5)

    # response = {"message": module_name}
    return jsonify(response), 200

# dimension-gen
@module_bp.route("/module/dimension-gen", methods=["POST"])
def dimension_gen():
    module_name = "dimension-gen"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    print(return_response)
    # time.sleep(5)

    message = []
    if return_response["status"] == "succeed":
        message.append(f"Detect {return_response["dimension_number"]} dimension notations.")
        
        current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
        session["currentDisplay"] = os.path.join(current_page.page_folder, "image", "dimension.png")
    else:
        message.append("No dimension notations detected.")

    response ={"status": True, 
               "message": message, 
               "currentDisplay": session["currentDisplay"]}

    # response = {"message": module_name}
    return jsonify(response), 200

# dimension-qc
@module_bp.route("/module/dimension-qc", methods=["POST"])
def dimension_qc():
    module_name = "dimension-qc"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    print(return_response)
    # time.sleep(5)

    message = []
    if return_response["status"] == "succeed":
        message.append(f"{return_response["correct"]} dimension notation are correct.")
        message.append(f"{return_response["total_check"] - return_response["correct"]} dimension notations are wrong.")
        
        current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
        session["currentDisplay"] = os.path.join(current_page.page_folder, "image", "dimension_qc.png")
    else:
        message.append("No dimension notations detected.")

    response ={"status": True, 
               "message": message, 
               "currentDisplay": session["currentDisplay"]}

    # response = {"message": module_name}
    return jsonify(response), 200
