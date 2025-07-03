import os
from pathlib import Path
from flask import Flask, request, send_file, make_response, send_from_directory
from flask import current_app, session, jsonify
import zipfile
from PyPDF2 import PdfMerger

from app.models import db, Page
from app.blueprints.report import report_bp


@report_bp.route("/report/qualitycontrol_download/<filetype>")
def qc_download(filetype):
    print(filetype)
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    session["current_orig_img_path"] = orig_img_path

    download_folder = current_app.config["SERVER_FOLDER"]
    # filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
    if filetype == "report": 
        # report
        filename = "qualitycontrol.pdf"
        sub_filepath = os.path.join(current_page.page_folder, filename)
        # return send_file(filepath, as_attachment=True, download_name=filename) 
        return send_from_directory(download_folder, sub_filepath, as_attachment=True)
    elif filetype == "separate": 
        zippath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "report.zip")
        print(zippath)
        with zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename in ["qualitycontrol.pdf", "qc_siteplan_appendix.pdf", "qc_ai_appendix.pdf"]:
                # filename = "qualitycontrol.pdf"
                filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
                zipf.write(filepath, arcname=filename)
        sub_zippath = os.path.join(current_page.page_folder, "report.zip")
        return send_from_directory(download_folder, sub_zippath, as_attachment=True)

    elif filetype == "combine":
        merger = PdfMerger()
        new_pdf_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "combine_report.zip")
        for filename in ["qualitycontrol.pdf", "qc_ai_appendix.pdf", "qc_siteplan_appendix.pdf"]:
            filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
            merger.append(filepath)
        merger.write(new_pdf_path)
        merger.close
        sub_filepath = os.path.join(current_page.page_folder, "combine_report.zip")
        return send_from_directory(download_folder, sub_filepath, as_attachment=True)
    # response = {"status": True}
    # return jsonify(response), 200

@report_bp.route("/report/costestimate_download/<filetype>")
def ce_download(filetype):
    print(filetype)
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    session["current_orig_img_path"] = orig_img_path

    download_folder = current_app.config["SERVER_FOLDER"]
    # filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
    if filetype == "report": 
        # report
        filename = "costestimate.pdf"
        sub_filepath = os.path.join(current_page.page_folder, filename)
        # return send_file(filepath, as_attachment=True, download_name=filename) 
        return send_from_directory(download_folder, sub_filepath, as_attachment=True)
    elif filetype == "separate": 
        zippath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "report.zip")
        print(zippath)
        with zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename in ["costestimate.pdf", "ce_appendix.pdf"]:
                # filename = "qualitycontrol.pdf"
                filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
                zipf.write(filepath, arcname=filename)
        sub_zippath = os.path.join(current_page.page_folder, "report.zip")
        return send_from_directory(download_folder, sub_zippath, as_attachment=True)

    elif filetype == "combine":
        merger = PdfMerger()
        new_pdf_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "combine_report.zip")
        for filename in ["costestimate.pdf", "ce_appendix.pdf"]:
            filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
            merger.append(filepath)
        merger.write(new_pdf_path)
        merger.close
        sub_filepath = os.path.join(current_page.page_folder, "combine_report.zip")
        return send_from_directory(download_folder, sub_filepath, as_attachment=True)
