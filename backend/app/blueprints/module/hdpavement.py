import os
from pathlib import Path
from flask import jsonify, session
import time

from app.models import db, Session, User, Page
from app.blueprints.module import module_bp
from app.blueprints.module.utils import simple_module_perform, simple_module_post


# heavyduty-pavement
@module_bp.route("/module/heavyduty-pavement", methods=["POST"])
def heavyduty_pavement():
    module_name = "heavyduty-pavement"
    print(module_name)
    # perform task
    simple_module_perform(module_name)
    # task func post
    return_response = simple_module_post(module_name)
    # time.sleep(5)

    message = []
    if return_response["status"] == "succeed":
        message.append(f"Totally heavy duty pavement area: {return_response["area"]} {return_response["unit"]}")

        current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
        session["currentDisplay"] = os.path.join(current_page.page_folder, "image", "heavyduty_pavement.png")
    else:
        message.append("No heavy duty pavement detected.")

    response = {"status": True, 
                "message": message, 
                "currentDisplay": session["currentDisplay"]}

    return jsonify(response), 200
