"""
Functions for heavy duty pavement cost estimate task.
"""
import os
from pathlib import Path
import cv2
import pandas as pd
import json
import numpy as np
import pickle

from siteplan_qualitycontrol.basic import detect_legend, save_legend, select_legend
from siteplan_qualitycontrol.ce_basic import heavyduty_pavement_detect, heavyduty_pavement_draw, heavyduty_pavement_measure
from siteplan_qualitycontrol.cost_estimate import cost_estimate_load

def heavyduty_pavement(
        orig_img_path: str = None):
    """
    Detect heavyduty pavement for cost estimate on siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    display_image = cv2.imread(orig_img_path)

    # do all heavy duty pavement detect on the body image
    body_image = cv2.imread(os.path.join(img_save_path, "body.png"))
    # find the heavy duty pavement legend
    paragraph_df = pd.read_csv(os.path.join(data_save_path, "paragraph.csv"))
    # search for keyword "HEAVY DUTY PAVEMENT", if not exist, go for "HEAVY DUTY ASPHALT PAVEMENT"
    legend_text_loc, legend_image_loc, legend_image = detect_legend(legend_name="HEAVY DUTY PAVEMENT", 
                                                                    source_image=body_image, 
                                                                    ocr_df=paragraph_df)
    if legend_image is None:
        legend_text_loc, legend_image_loc, legend_image = detect_legend(legend_name="HEAVY DUTY ASPHALT PAVEMENT", 
                                                                        source_image=body_image, 
                                                                        ocr_df=paragraph_df)
    # to cases with no heavy duty pavement legend detected
    if legend_image is None:
        heavyduty_pavement_info = {"status": "fail", 
                                   "error message": "no heavy duty pavement legend detected."}
        # save the results
        with open(os.path.join(data_save_path, "heavyduty_pavement.json"), "w") as fp:
            json.dump(heavyduty_pavement_info, fp, indent=4)
        return None
    
    # save the heavy duty pavement legend
    save_legend(legend_name="heavy_duty_pavement", 
                legend_text_loc=legend_text_loc, 
                legend_image_loc=legend_image_loc, 
                legend_image=legend_image, 
                data_save_path=data_save_path)
    
    # detect contours for all heavypavement
    contours = heavyduty_pavement_detect(body_image, legend_image, legend_image_loc)
    with open(os.path.join(data_save_path, "heavyduty_pavement.pkl"), "wb") as f:
        pickle.dump(contours, f)

    # draw the image
    # read the legend
    hd_pavement_legend_series = select_legend(legend_name="heavy_duty_pavement", data_save_path=data_save_path)
    hd_pavement_image = heavyduty_pavement_draw(contours, display_image, hd_pavement_legend_series)
    cv2.imwrite(os.path.join(img_save_path, "heavyduty_pavement.png"), hd_pavement_image)

    # read in the scale information
    with open(os.path.join(data_save_path, "scale.json"), "r") as fp:
        scale_info = json.load(fp)

    # calculate area (in sf)
    area = heavyduty_pavement_measure(orig_img_path, contours, scale_info)

    heavyduty_pavement_info = {"status": "succeed", 
                               "area": area, 
                               "unit": "SF"}
    # save the results
    with open(os.path.join(data_save_path, "heavyduty_pavement.json"), "w") as fp:
        json.dump(heavyduty_pavement_info, fp, indent=4)

    # update the results in cost estimate form
    ce_form = cost_estimate_load(orig_img_path)
    ce_form.quantity_update(sheet_name="offsite", 
                            description="Heavy duty", 
                            quantity=heavyduty_pavement_info["area"], 
                            input_unit=heavyduty_pavement_info["unit"])


def heavyduty_pavement_post(
        orig_img_path: str = None):
    """
    Return results for heavy duty pavement task on siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load heavy duty pavement information
    with open(os.path.join(data_save_path, "heavyduty_pavement.json"), "r") as fp:
        hd_pavement_info = json.load(fp)

    return hd_pavement_info