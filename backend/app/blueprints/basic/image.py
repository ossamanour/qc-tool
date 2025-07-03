import os
from flask import jsonify, send_from_directory
from flask import current_app, session

from app.models import db, Page
from app.blueprints.basic import basic_bp


# image display
@basic_bp.route("/image/<path:filename>")
def server_image(filename):
    print(filename)
    return send_from_directory(current_app.config["SERVER_FOLDER"], filename)


# switch between pages
@basic_bp.route("/image/previous_page", methods=["POST"])
def previous_page():
    # change current page
    total_page = session["currentSession"]["total_page"]
    current_page = session["currentPage"]
    if current_page == 1:
        previous_page = total_page
    else:
        previous_page = current_page - 1
    session["currentPage"] = previous_page

    # change current display
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    session["currentDisplay"] = os.path.join(current_page.page_folder, "original.png")

    response = {"status": True, 
                "currentPage": session["currentPage"], 
                "currentDisplay": session["currentDisplay"]}
    return jsonify(response), 200


@basic_bp.route("/image/next_page", methods=["POST"])
def next_page():
    # change current page
    total_page = session["currentSession"]["total_page"]
    current_page = session["currentPage"]
    if current_page == total_page:
        next_page = 1
    else:
        next_page = current_page + 1
    session["currentPage"] = next_page

    # change current display
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    session["currentDisplay"] = os.path.join(current_page.page_folder, "original.png")

    response = {"status": True, 
                "currentPage": session["currentPage"], 
                "currentDisplay": session["currentDisplay"]}
    return jsonify(response), 200