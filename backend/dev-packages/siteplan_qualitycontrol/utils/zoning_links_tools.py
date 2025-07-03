"""
Tools related to zoning links (in assets folder).
"""
import os
from siteplan_qualitycontrol.utils import global_var
import json

def load_zoning_links():
    """
    Load the zoning links from file.

    @return: zoning_links: dictionary containing zoning links.
    """
    filepath = os.path.join(global_var.ROOT, "assets", "zoning_links.json")
    with open(filepath, "r") as fp:
        zoning_links = json.load(fp)

    return zoning_links

def get_zoning_url_attribute(
        city: str = None):
    """
    Get the zoning url and corresponding attribute from city name.

    @param: city: city name.

    @return: city_url_attribute: dictionary containing url and attribute of given city.
    """
    zoning_links = load_zoning_links()
    city = city.capitalize()
    city_url_attribute = zoning_links[city]

    return city_url_attribute

def modify_zoning_url(
        zoning_url: str = None,
        loc: tuple = None):
    """
    Modify the url with correct coordinates.

    @param: zoning_url: url for zoning.
    @param: loc: tuple containing coordinates.

    @return: zoning_url: modified url.
    """
    (x_min, x_max, y_min, y_max) = loc
    zoning_url = zoning_url.replace("[x_min]", str(x_min))
    zoning_url = zoning_url.replace("[x_max]", str(x_max))
    zoning_url = zoning_url.replace("[y_min]", str(y_min))
    zoning_url = zoning_url.replace("[y_max]", str(y_max))
    
    return zoning_url

def get_and_modify_county_coordinates_url(
        county: str = None, 
        loc: tuple = None):
    """
    Get the county url and modify with location information or apn.

    @param: name: url name.
    @param: loc: tuple of location information, (x, y).

    @return: county_url: modified url.
    """
    zoning_links = load_zoning_links()
    if county.capitalize() == "Maricopa":
        county_url = zoning_links["maricopa_coordinates_url"]
        (x, y) = loc
        county_url = county_url.replace("[x]", str(x))
        county_url = county_url.replace("[y]", str(y))

    return county_url
