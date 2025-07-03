"""
Perform body sidebar module.
"""
import os
from pathlib import Path
import json
import cv2
import json

from siteplan_qualitycontrol.company_config import COMPANY_FUNC_LISTS


def body_sidebar_generate(
        orig_img_path: str = None):
    """
    Prepare the siteplan/landscape image for later analysis by seperate them into main-body and side-bar using templates.

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

    # get the main portion and the sidebar protion using template
    body_sidebar_generate = COMPANY_FUNC_LISTS.get(company).get("body_generate")
    body_image, sidebar_image = body_sidebar_generate(original_image)
    cv2.imwrite(os.path.join(img_save_path, "body.png"), body_image)
    cv2.imwrite(os.path.join(img_save_path, "sidebar.png"), sidebar_image)
