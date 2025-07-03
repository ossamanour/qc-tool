"""
Perform information generation (detection) module.
"""
import os
from pathlib import Path
import json
import cv2
import numpy as np

from siteplan_qualitycontrol.company_config import COMPANY_FUNC_LISTS
from siteplan_qualitycontrol.analysis import apn_generate


def information_generate(
        orig_img_path: str = None):
    """
    Detect basic information from siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # read the config file to choose which compnay template is used
    with open(os.path.join(Path(orig_img_path).parents[1], "config.json"), "r") as fp:
        config = json.load(fp)
        company = config["company"]

    # read in the sidebar image
    sidebar_image = cv2.imread(os.path.join(img_save_path, "sidebar.png"))

    # get information
    info_generate = COMPANY_FUNC_LISTS.get(company).get("info_generate")
    information = info_generate(original_image)

    # box out the information
    display_image = cv2.imread(orig_img_path)
    for key in information["contours"]:
        contour = np.array(information["contours"][key])
        cv2.drawContours(display_image, [contour], -1, (255, 0, 255), 2)
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.putText(display_image, key, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.imwrite(os.path.join(img_save_path, "information.png"), display_image)

    # get the apn information if exist, add apn information in the information dictionary
    apn_list = apn_generate(orig_img_path)
    information["apn_list"] = apn_list

    with open(os.path.join(data_save_path, "information.json"), "w") as fp:
        json.dump(information, fp, indent=4)
    # print(information)


def information_post(
        orig_img_path: str = None):
    """
    Return detected information on the siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load information
    with open(os.path.join(data_save_path, "information.json"), "r") as fp:
        information = json.load(fp)
    
    return_info = {"title": information["title"], 
                   "address": information["address"], 
                   "apn_list": information["apn_list"]}
    return return_info
