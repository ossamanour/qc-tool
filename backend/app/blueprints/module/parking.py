import os
from flask import jsonify, session
import time

from app.models import db, Session, User, Page
from app.blueprints.module import module_bp
from app.blueprints.module.utils import simple_module_perform, simple_module_post


# parking count
@module_bp.route("/module/parking-count", methods=["POST"])
def parking_count():
    module_name = "parking-count"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    print(return_response)
    # time.sleep(5)

    message = []
    if return_response["status"] == "succeed":
        message.append(f"Total proposed parking spaces: {return_response["total_parking"]}.")

        current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
        session["currentDisplay"] = os.path.join(current_page.page_folder, "image", "parking_count.png")
    else:
        message.append("No parking spaces detected.")

    response = {"status": True, 
                "message": message, 
                "currentDisplay": session["currentDisplay"]}

    return jsonify(response), 200