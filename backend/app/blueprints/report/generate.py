import os
from pathlib import Path
from io import BytesIO
from flask import Flask, request, send_file, make_response
from flask import current_app, session, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch

from app.models import db, Page
from app.blueprints.report import report_bp
from app.blueprints.report import get_project_information, get_dimension_control
from app.blueprints.report import get_parking_control, get_parking_cahtbot
from app.blueprints.report import QualityControlReport, CostEstimateReport, AppendixReport
from siteplan_qualitycontrol.ce_basic import CostEstimateForm
from siteplan_qualitycontrol.utils import LogJson


@report_bp.route("/report/qualitycontrol_tasklist")
def qc_task_list():
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    session["current_orig_img_path"] = orig_img_path
    # read in process log
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    task_list = []
    if process_log.check("zoning"):
        task_list.append({
            "label": "ZONING", 
            "value": "ZONING", 
            "checked": False})
    if process_log.check("dimension-qc"):
        task_list.append({
            "label": "DIMENSION", 
            "value": "DIMENSION", 
            "checked": False})
    if process_log.check("keynote-gen"):
        task_list.append({
            "label": "KEYNOTE-MATCH", 
            "value": "KEYNOTE-MATCH", 
            "checked": False})
    if process_log.check("parking-count"):
        task_list.append({
            "label": "PARKING", 
            "value": "PARKING", 
            "checked": False})

    response = {"status": True, 
                "taskList": task_list}
    return jsonify(response), 200


@report_bp.route("/report/qualitycontrol_generate", methods=["POST"])
def qc_report_generate():
    data = request.get_json()
    submitted_tasks = data
    print(submitted_tasks)
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    session["current_orig_img_path"] = orig_img_path
    # folder for report
    report_folder = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder)

    # create an instance for main report
    qc_report = QualityControlReport(
        id="main",
        pagesize=letter, 
        topMargin=1*inch, 
        leftMargin=0.5*inch, 
        rightMargin=0.5*inch, 
        bottomMargin=1*inch)
    # create an instance for ai appendix report
    ai_appen_report = QualityControlReport(
        id="ai-appendix",
        pagesize=letter, 
        topMargin=1*inch, 
        leftMargin=0.5*inch, 
        rightMargin=0.5*inch, 
        bottomMargin=1*inch)
    # create an instance for appendix report
    appen_report = AppendixReport(
        id="appendix",
        pagesize=(36*inch, 24*inch), 
        topMargin=0, 
        leftMargin=0, 
        rightMargin=0, 
        bottomMargin=0)
    appen_report.make_coverpage("Site Plan Appendix for Quality Control")

    # make title for report
    qc_report.make_title(title="Quality CONTROL REPORT")

    # make title for ai appendix
    ai_appen_report.make_title(title="AI Appendix for Quality Control")

    # add basic information
    basic_info_data = get_project_information(orig_img_path)
    qc_report.make_horizontal_table(
        heading="project information", 
        data=basic_info_data, 
        colWidth=[2.5*inch, 5*inch])
    
    appendix_page_number = 2

    if "DIMENSION" in submitted_tasks:
        # dimension quality control results
        qc_report.make_section_header("dimension quality control")
        
        info_list_data, results_list_data, _, dimension_info = get_dimension_control(
            orig_img_path, current_page.page_folder)
        qc_report.make_subsecion_header("provided information:")
        qc_report.make_subsection_bullet_list(info_list_data)
        qc_report.make_subsection_bullet_hyperlink(
            link=f'http://localhost:5173/api/report/download/{os.path.join(current_page.page_folder, f"qc_siteplan_appendix.pdf#page={appendix_page_number}").replace("/", 'FLAG_EXTRA')}', 
            text="Site Plan Appendix"
        )
        appendix_page_number = appendix_page_number + 1
        # add image to appendix
        if dimension_info is not None:
            appen_report.make_newpage()
            appen_report.make_image(
                title="dimension quality control image", 
                image_path=dimension_info["image_path"], 
                width=33*inch, 
                height=22*inch)

        qc_report.make_subsecion_header("quality control results:")
        qc_report.make_subsection_bullet_list(results_list_data)

    if "PARKING" in submitted_tasks:
        # parking quality control results
        qc_report.make_section_header("parking quality control")
        
        parking_list_data, parking_info = get_parking_control(orig_img_path)
        qc_report.make_subsecion_header("provided information:")
        qc_report.make_subsection_bullet_list(parking_list_data)
        
        info_list_data, results_list_data, ai_ref_list_data, parking_chatbot_info = get_parking_cahtbot(orig_img_path)
        qc_report.make_subsection_bullet_list(info_list_data)
        qc_report.make_subsection_bullet_hyperlink(
            link=f'http://localhost:5173/api/report/download/{os.path.join(current_page.page_folder, f"qc_siteplan_appendix.pdf#page={appendix_page_number}").replace("/", 'FLAG_EXTRA')}', 
            text="Site Plan Appendix"
        )
        appendix_page_number = appendix_page_number + 1
        # add image to appendix
        if parking_info is not None:
            appen_report.make_newpage()
            appen_report.make_image(
                title="parking count image", 
                image_path=parking_info["image_path"], 
                width=33*inch, 
                height=22*inch)

        qc_report.make_subsecion_header("quality control results:")
        qc_report.make_subsection_bullet_list(results_list_data)
        qc_report.make_subsection_bullet_hyperlink(
            link=f'http://localhost:5173/api/report/download/{os.path.join(current_page.page_folder, f"qc_ai_appendix.pdf#page={appendix_page_number}").replace("/", 'FLAG_EXTRA')}', 
            text="AI Appendix"
        )
        
        ai_appen_report.make_section_header("parking quality control")
        ai_appen_report.make_subsecion_header("reference information from AI:")
        ai_appen_report.make_subsection_bullet_list(ai_ref_list_data)

    # build and save
    # report
    filename = "qualitycontrol.pdf"
    filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
    qc_report.build_and_save(filepath)

    # ai appendix
    filename = "qc_ai_appendix.pdf"
    filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
    ai_appen_report.build_and_save(filepath)

    # siteplan appendix
    filename = "qc_siteplan_appendix.pdf"
    filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
    appen_report.build_and_save(filepath)
    
    return send_file(filepath, as_attachment=True, download_name=filename)


@report_bp.route("/report/costestimate_tasklist")
def ce_task_list():
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    session["current_orig_img_path"] = orig_img_path
    # read in process log
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    response = {"status": True, 
                "taskList": []}
    return jsonify(response), 200


@report_bp.route("/report/costestimate_generate", methods=["POST"])
def ce_report_generate():
    # get the current page information
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    session["current_orig_img_path"] = orig_img_path
    # folder for report
    report_folder = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder)

    # create an instance for main report 
    ce_report = CostEstimateReport(
        id="main",
        pagesize=letter, 
        topMargin=1*inch, 
        leftMargin=0.5*inch, 
        rightMargin=0.5*inch, 
        bottomMargin=1*inch)
    # create an instance for appendix report
    appen_report = AppendixReport(
        id="appendx",
        pagesize=(36*inch, 24*inch), 
        topMargin=0, 
        leftMargin=0, 
        rightMargin=0, 
        bottomMargin=0)
    appen_report.make_coverpage("Site Plan Appendix for Cost Estimate")

    # make title
    ce_report.make_title(title="Cost Estimate report")

    # load tables
    # cost estimate form path
    cost_estimate_form_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "cost_estimate.xlsx")
    # load the sheet
    cost_estimate_form = CostEstimateForm(cost_estimate_form_path)
    onsite_df = cost_estimate_form.onsite_df
    offsite_df = cost_estimate_form.offsite_df
    onsite_df.fillna("", inplace=True)
    offsite_df.fillna("", inplace=True)
    
    ce_report.make_cost_table("On-site", onsite_df)
    ce_report.make_cost_table("Off-site", offsite_df)

    ce_report.make_subsection_bullet_hyperlink(
        link=f'http://localhost:5173/api/report/download/{os.path.join(current_page.page_folder, "ce_appendix.pdf").replace("/", 'FLAG_EXTRA')}', 
        text="Site Plan Appendix"
    )

    # appendix
    # read in process log
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    if process_log.check("heavyduty-pavement"):
        appen_report.make_newpage()
        appen_report.make_image(
            title="heavyduty pavement reference image", 
            image_path=os.path.join(Path(orig_img_path).parent, "image", "heavyduty_pavement.png"), 
            width=33*inch, 
            height=22*inch)
    
    if process_log.check("ada-ramp"):
        appen_report.make_newpage()
        appen_report.make_image(
            title="ADA Ramp reference image", 
            image_path=os.path.join(Path(orig_img_path).parent, "image", "ada_ramp.png"), 
            width=33*inch, 
            height=22*inch)
    
    if process_log.check("ada-sign"):
        appen_report.make_newpage()
        appen_report.make_image(
            title="ADA sign reference image", 
            image_path=os.path.join(Path(orig_img_path).parent, "image", "ada_sign.png"), 
            width=33*inch, 
            height=22*inch)
        
    if process_log.check("fire-hydrant"):
        appen_report.make_newpage()
        appen_report.make_image(
            title="fire hydrant reference image", 
            image_path=os.path.join(Path(orig_img_path).parent, "image", "fire_hydrant.png"), 
            width=33*inch, 
            height=22*inch)
        
    if process_log.check("light-pole"):
        appen_report.make_newpage()
        appen_report.make_image(
            title="light pole reference image", 
            image_path=os.path.join(Path(orig_img_path).parent, "image", "light_pole.png"), 
            width=33*inch, 
            height=22*inch)

    # build and save
    ce_report.build()
    filename = "costestimate.pdf"
    filepath = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, filename)
    ce_report.save(filepath=filepath)

    # build
    appen_report.build()
    appen_name = "ce_appendix.pdf"
    appen_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, appen_name)
    appen_report.save(filepath=appen_path)
    
    return send_file(filepath, as_attachment=True, download_name=filename)