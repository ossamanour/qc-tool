"""
Global variables definition.
"""

import os
from pathlib import Path


# list containing all possible keynote title
KEYNOTE_LIST_TITLE = {0: "SITE PLAN KEYNOTES", 
                      1: "SITE PLAN KEY NOTES", 
                      2: "SITE PLAN NOTES", 
                      3: "REMOVAL CONSTRUCTION KEY NOTES", 
                      4: "PLAN NOTES"}

# allowed chars when doing ocr analysis on siteplan
ALLOWED_CHARS = set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.!=—\"\'\’°§()<>-&:/@%\”"))

# dictionary for the city_county corresponding relationship
CITY_COUNTY = {"SCOTTSDALE": ["MARICOPA"], 
               "PHOENIX": ["MARICOPA"], 
               "ELOY": ["PINAL"], 
               "GLENDALE": ["MARICOPA"], 
               "MESA": ["MARICOPA"], 
               "FLAGSTAFF": ["COCONINO"], 
               "PEORIA": ["MARICOPA"], 
               "TEMPE": ["MARICOPA"], 
               "GILBERT": ["MARICOPA"], 
               "AVONDALE": ["MARICOPA"]} 

# list containing all cities that currently quality control support
SUPPORT_CITY = ["SCOTTSDALE", 
                "GILBERT"]

# root directory
ROOT = Path(os.path.abspath(__file__)).parents[2]