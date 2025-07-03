from flask import jsonify
import time

from app.blueprints.module import module_bp
from app.blueprints.module.utils import simple_module_perform, simple_module_post


# body-sidebar
@module_bp.route("/module/body-sidebar", methods=["POST"])
def body_sidebar():
    module_name = "body-sidebar"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    response = simple_module_post(module_name)
    # time.sleep(5)
    
    response = {"status": True}
    return jsonify(response), 200

# body-ocr
@module_bp.route("/module/body-ocr", methods=["POST"])
def body_ocr():
    module_name = "body-ocr"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    response = simple_module_post(module_name)
    # time.sleep(5)

    response = {"status": True}
    return jsonify(response), 200


# keynote-match-pre
@module_bp.route("/module/keynote-match-pre", methods=["POST"])
def keynote_match_pre():
    module_name = "keynote-match-pre"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    # time.sleep(5)
    
    response = {"status": True}
    return jsonify(response), 200

# costestimate-prepare
@module_bp.route("/module/costestimate-prepare", methods=["POST"])
def costestimate_prepare():
    module_name = "costestimate-prepare"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    # time.sleep(5)
    
    response = {"status": True}
    return jsonify(response), 200

