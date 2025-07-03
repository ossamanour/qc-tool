"""
Functions of tools for parking requirement.
"""
import os
import pandas as pd

from siteplan_qualitycontrol.utils import global_var


def parking_requirement_call(
        city: str = None, 
        zone: str = None):
    """
    Get the parking requirement for the input city and zone, local database.

    @param: city: city name.
    @param: zong: zone code, need to be modified to match the database notation.

    @return: parking_requirement: dataframe containing parking requirement.
    """
    rootdir = os.path.join(global_var.ROOT, "assets", "city_rules", city.lower())

    if city.upper() not in global_var.SUPPORT_CITY:
        return None

    # for different cities, there are different ways to call the requirement
    if city.lower() == "scottsdale":
        # scottsdale has different landuse types for downtown zoning and other zoning
        if zone == "(D)":
            municode_csv_path = os.path.join(rootdir, "parking_downtown.csv")
        else:
            municode_csv_path = os.path.join(rootdir, "parking_other.csv")
    elif city.lower() == "gilbert":
        municode_csv_path = os.path.join(rootdir, "parking.csv")
    
    # load municode
    parking_requirement = pd.read_csv(municode_csv_path)

    return parking_requirement

