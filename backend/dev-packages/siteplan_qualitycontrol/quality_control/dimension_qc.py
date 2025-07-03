"""
Functions for dimension quality control task.
"""
import os
from pathlib import Path
import json
import cv2
from ast import literal_eval
import pandas as pd

from siteplan_qualitycontrol.qc_basic import dimension_check, dimension_qc_draw


def dimension_quality_control(
        orig_img_path: str = None):
    """
    Function to perform dimension quality control on the give siteplan iamge.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    original_image = cv2.imread(orig_img_path)

    # load the dimsnion generation information
    with open(os.path.join(data_save_path, "dimension.json"), "r") as fp:
        dimension_info = json.load(fp)

    if dimension_info["status"] == "fail": 
        # no dimension, then, no check needed
        dimension_qc_info = {"status": "fail", 
                             "error message": dimension_info["error message"]}

        # save the results
        with open(os.path.join(data_save_path, "dimension_qc.json"), "w") as fp:
            json.dump(dimension_qc_info, fp, indent=4)
        
        return
    
    # normal dimension qc for detected dimensions
    # for cases with dimensions, get the dimension arrow arrow pair index
    dimension_arrow_pairs = dimension_info["dimension_arrow_pairs"]

    # read in arrow information
    arrow_angle_df = pd.read_csv(os.path.join(data_save_path, "arrow_angle.csv"), 
                                 converters={'contour': literal_eval, 
                                             'tip_pt': literal_eval, 
                                             'mid_pt': literal_eval})
    
    # read in the scale information
    with open(os.path.join(data_save_path, "scale.json"), "r") as fp:
        scale_info = json.load(fp)

    # measure, read and check the dimensions
    dimension_qc_results_df = dimension_check(dimension_arrow_pairs, arrow_angle_df, scale_info, original_image)
    dimension_qc_results_df.to_csv(os.path.join(data_save_path, "dimension_qc.csv"), index=False)
    
    # draw the results
    dimension_qc_image = dimension_qc_draw(dimension_qc_results_df, original_image, arrow_angle_df)
    cv2.imwrite(os.path.join(img_save_path, "dimension_qc.png"), dimension_qc_image)

    # generate the information dict
    dimension_qc_info = {"status": "succeed", 
                         "total_check": int(len(dimension_qc_results_df)), 
                         "correct": int(dimension_qc_results_df.check.values.sum())}
    # save the results
    with open(os.path.join(data_save_path, "dimension_qc.json"), "w") as fp:
        json.dump(dimension_qc_info, fp, indent=4)


def dimension_quality_control_post(
        orig_img_path: None):
    """
    Function to return the results of dimension quality control task.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.

    @return: dimension_qc_info: JSON containing results for dimension quality control task.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load dimension qc information
    with open(os.path.join(data_save_path, "dimension_qc.json"), "r") as fp:
        dimension_qc_info = json.load(fp)

    return dimension_qc_info


