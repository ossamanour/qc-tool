"""
Perform arrow generate module.
"""
import os
from pathlib import Path
import cv2
import json
import pandas as pd

from siteplan_qualitycontrol.images import arrow_tip_template_call
from siteplan_qualitycontrol.utils import dataframe_save
from siteplan_qualitycontrol.basic import arrow_tip_search, arrow_tip_angle, arrow_tip_draw


def arrow_generate(
        orig_img_path: str = None):
    """
    Detect all arrows, using template, from the siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    display_image = cv2.imread(orig_img_path)

    # do arrow tip search on the body image 
    image = cv2.imread(os.path.join(img_save_path, "body.png"))
    arrow_tip_template = cv2.imread(arrow_tip_template_call())
    arrow_tip_df = arrow_tip_search(image, arrow_tip_template)
    if len(arrow_tip_df) == 0:
        arrow_info = {"status": "fail", 
                      "error message": "no arrow tips detected"}
        with open(os.path.join(data_save_path, "arrow.json"), "w") as fp:
            json.dump(arrow_info, fp, indent=4)
        return None
    dataframe_save(arrow_tip_df, os.path.join(data_save_path, "arrow.csv"))
    arrow_tip_image = arrow_tip_draw(arrow_tip_df, display_image, with_angle=False)
    cv2.imwrite(os.path.join(img_save_path, "arrow.png"), arrow_tip_image)

    # calculate angle of each arrow tip
    arrow_tip_angle_df = arrow_tip_angle(arrow_tip_df)
    dataframe_save(arrow_tip_angle_df, os.path.join(data_save_path, "arrow_angle.csv"))
    # draw the image with arrow tip and angle information    
    arrow_tip_angle_image = arrow_tip_draw(arrow_tip_angle_df, display_image, with_angle=True)
    cv2.imwrite(os.path.join(img_save_path, "arrow_angle.png"), arrow_tip_angle_image)

    # create information
    arrow_info = {"status": "succeed", 
                  "arrow_number": len(arrow_tip_df)}
    # save the results
    with open(os.path.join(data_save_path, "arrow.json"), "w") as fp:
        json.dump(arrow_info, fp, indent=4)


def arrow_generate_post(
        orig_img_path: str = None):
    """
    Return information of all detected arrows on the siteplan.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load arrow generation information
    with open(os.path.join(data_save_path, "arrow.json"), "r") as fp:
        arrow_generate_info = json.load(fp)

    return arrow_generate_info



