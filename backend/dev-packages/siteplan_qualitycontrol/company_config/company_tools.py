"""
Functions of tools for company template.
"""
import os
from pathlib import Path

from siteplan_qualitycontrol.utils import global_var


def list_all_company_template():
    """
    List names of all supported company templates.

    @return: company_list: list of names of all supported companies.
    """
    path = os.path.join(global_var.ROOT, "assets", "companies")

    company_list = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

    return company_list
