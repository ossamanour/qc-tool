"""
Functions of tools for zone codes related.
"""
import os
import json

from siteplan_qualitycontrol.utils import global_var


def zone_list_call(
        city: str = None):
    """
    List all available zoning codes for the given city.

    @param: city: city name.

    @return:city_zone: all available zoning codes.
    """
    rootdir = os.path.join(global_var.ROOT, "assets", "city_rules")

    zone_codes_file_path = os.path.join(rootdir, "zone_codes_new.json")
    with open(zone_codes_file_path, "r") as fp:
        zone_codes = json.load(fp)
    city_zone = zone_codes[city.title()]
    
    return city_zone


def zone_check(
        zone: str = None, 
        city: str = None):
    """
    Check if the input zone code is available in the input city.

    @param: zone: zone code.
    @param: city: city name.

    @return: JSON including check results. 
    """
    city_zone = zone_list_call(city)

    if city.upper() not in global_var.SUPPORT_CITY:
        return {"status:": "fail", 
                "error message": "city not supported"}

    # gilbert
    if city.title() == "Gilbert":
        if zone in city_zone.keys():
            return {"status": "succeed", 
                    "zone": zone}
        else: 
            return {"status:": "fail", 
                    "error message": "zone not exist"}

    # scottdale
    if city.title() == "Scottsdale":
        if zone in city_zone.keys():
            return zone
        else:
            modified_zone = f"({zone})"
            if modified_zone in city_zone.keys():
                return {"status": "succeed", 
                        "zone": modified_zone}
            else:
                return {"status:": "fail", 
                        "error message": "zone not exist"}