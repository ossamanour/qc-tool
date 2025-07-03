"""
Functions related to cost estimate form.
"""
import os
from pathlib import Path

from siteplan_qualitycontrol.utils import ProjectConfigJson
from siteplan_qualitycontrol.ce_basic import CostEstimateForm


def cost_estimate_prepare(
        orig_img_path: str = None):
    """
    Prepare cost estimate for the current siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the project config
    project_config_path = os.path.join(Path(orig_img_path).parents[1], "config.json")
    project_config = ProjectConfigJson(project_config_path).config_json

    # copy the price sheet template to the page folder
    cost_estimate_form_path = os.path.join(Path(orig_img_path).parent, "cost_estimate.xlsx")
    cost_estimate_form = CostEstimateForm(cost_estimate_form_path, project_config["price_sheet"])


def cost_estimate_load(
        orig_img_path: str = None):
    """
    Load the cost estimate form for the current siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    cost_estimate_form_path = os.path.join(Path(orig_img_path).parent, "cost_estimate.xlsx")
    cost_estimate_form = CostEstimateForm(cost_estimate_form_path)

    return cost_estimate_form
