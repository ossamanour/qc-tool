import os
from pathlib import Path
import pandas as pd
from flask import Blueprint, jsonify
from flask import request, current_app, session
from collections import OrderedDict

from app.models import db, Page
from siteplan_qualitycontrol.ce_basic import list_all_price_sheet_templates, price_sheet_template_load
from siteplan_qualitycontrol.ce_basic import CostEstimateForm
from app.blueprints.basic import basic_bp


@basic_bp.route("/pricesheet/load_current", methods=["POST"])
def pricesheet_load_current():
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()

    # cost estimate form path
    cost_estimate_form_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "cost_estimate.xlsx")

    # load the sheet
    cost_estimate_form = CostEstimateForm(cost_estimate_form_path)
    onsite_df = cost_estimate_form.onsite_df
    offsite_df = cost_estimate_form.offsite_df
    onsite_df.fillna("", inplace=True)
    offsite_df.fillna("", inplace=True)
    print(onsite_df)

    response = {"status": True, 
                "sheetHeader": list(onsite_df), 
                "onsiteSheet": onsite_df.to_dict(orient="records", into=OrderedDict), 
                "offsiteSheet": offsite_df.to_dict(orient="records", into=OrderedDict)}
    return jsonify(response), 200
