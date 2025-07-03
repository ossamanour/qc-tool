import os
from pathlib import Path
import pandas as pd

from siteplan_qualitycontrol.utils import global_var


def list_all_price_sheet_templates():
    rootdir = os.path.join(global_var.ROOT, "assets", "price_sheets")
    template_list = os.listdir(rootdir)
    return template_list


def price_sheet_template_load(
        template_name: str = None):
    rootdir = os.path.join(global_var.ROOT, "assets", "price_sheets")
    template_path = os.path.join(rootdir, template_name)

    template_df = pd.read_csv(template_path)

    return template_df
    

