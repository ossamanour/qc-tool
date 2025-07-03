"""
Functions of tools for cost estimate price sheet template
"""
import os
from pathlib import Path
import pandas as pd

from siteplan_qualitycontrol.utils import global_var


def list_all_price_sheet_templates():
    """
    List names of all available price sheet templates.

    @return: template_list: list of names of all available price sheet templates.
    """
    rootdir = os.path.join(global_var.ROOT, "assets", "price_sheets")
    template_list = os.listdir(rootdir)
    return template_list


def price_sheet_template_load(
        template_name: str = None):
    """
    Load the price sheet template by name.

    @param: template_name: name of the price sheet.

    @return: template_form: dataframe containing the loaded price sheet template.
    """
    rootdir = os.path.join(global_var.ROOT, "assets", "price_sheets")
    template_path = os.path.join(rootdir, template_name)

    # template_df = pd.read_csv(template_path)
    template_form = pd.read_excel(template_path, sheet_name=None)

    return template_form
    

