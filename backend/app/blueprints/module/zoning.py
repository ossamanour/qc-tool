from flask import jsonify

from app.blueprints.module import module_bp
from app.blueprints.module.utils import simple_module_perform, simple_module_post


# info-gen
@module_bp.route("/module/info-gen", methods=["POST"])
def info_gen():
    module_name = "info-gen"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    # time.sleep(5)

    message = []
    message.append(f"Project Title: {return_response["title"]}")
    if return_response["address"] != "":
        message.append(f"Address: {return_response["address"]}")
    if return_response["apn_list"] != []:
        message.append(f"APN: {return_response["apn_list"]}")

    response ={"status": True, 
               "message": message}

    # response = {"message": "info-gen"}
    return jsonify(response), 200


# zoning
@module_bp.route("/module/zoning", methods=["POST"])
def zoning():
    module_name = "zoning"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    # time.sleep(5)

    message = []
    if return_response["status"] == "succeed":
        message.append(f"Detect zone from {return_response["source"]}: {return_response["zone"]}")
    else:
        message.append("No zone information detected")

    response ={"status": True, 
               "message": message}
    
    # response = {"message": "info-gen"}
    return jsonify(response), 200
