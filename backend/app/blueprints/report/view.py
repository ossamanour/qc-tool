import os
from pathlib import Path
from flask import send_file, jsonify, send_from_directory
from flask import current_app, session

from app.models import db, Page
from app.blueprints.report import report_bp


# view report
@report_bp.route("/report/view/<filename>")
def view_report(filename):
    print(filename)
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # folder
    folderpath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder)
    filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
    print(filepath)
    if os.path.exists(filepath):
        # return send_file(filepath, as_attachment=True)
        return send_from_directory(folderpath, filename)
    else:
        return jsonify({"error": "File not exist."}), 404

# download report
@report_bp.route("/report/download/<filename>")
def download_report(filename):
    print(filename)
    filename = filename.replace('FLAG_EXTRA', "/")
    
    # folder
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # folder 
    folder_path = current_app.config["SERVER_FOLDER"]
    filepath = os.path.join(folder_path, filename)
    if os.path.exists(filepath):
        return send_from_directory(folder_path, filename)
    else:
        return jsonify({"error": "File not exist."}), 404