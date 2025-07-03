"""
Functions of tools for building height requirement.
"""
import os
import pandas as pd
import json

from siteplan_qualitycontrol.utils import global_var


def height_requirement_call(
        city: str = None, 
        zone: str = None):
    """
    Get the building height requirement for the input city and zone, local database.

    @param: city: city name.
    @param: zong: zone code, need to be modified to match the database notation.

    @return: height_requirement: dictionary containing building height requirement.
    """
    rootdir = os.path.join(global_var.ROOT, "assets", "city_rules", city.lower())

    if city.upper() not in global_var.SUPPORT_CITY:
        return None
    
    municode_json_path = os.path.join(rootdir, "building_height.json")

    with open(municode_json_path, "r") as fp:
        city_height_requirement = json.load(fp)

    height_requirement = city_height_requirement[zone]

    return height_requirement
    
