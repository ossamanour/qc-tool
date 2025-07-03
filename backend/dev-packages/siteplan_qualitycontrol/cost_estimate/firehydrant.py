"""
Functions for fire hydrant cost etsimate task.
"""
import os
from pathlib import Path
import cv2
import pandas as pd
import json
import pickle

from siteplan_qualitycontrol.ce_basic import get_keynote_with_words_sets, keynote_match_draw
from siteplan_qualitycontrol.ce_basic import FIREHYDRANT_SET
from siteplan_qualitycontrol.basic import single_keynote_match
from siteplan_qualitycontrol.utils import keynote_read_csv
from siteplan_qualitycontrol.cost_estimate import cost_estimate_load


def fire_hydrant(
        orig_img_path: str = None):
    """
    Detect fire hydrant for cost estimate on siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    display_image = cv2.imread(orig_img_path)

    # read in the keynote pair information
    with open(os.path.join(data_save_path, "keynote.json"), "r") as fp:
        keynote_info = json.load(fp)

    keynote_df_path = os.path.join(keynote_info["key_folder"], "keynote.csv")
    keynote_df = keynote_read_csv(keynote_df_path)
    keynote_folder = keynote_info["key_folder"]

    # detect if there is a keynote for 'fire hydrant'
    keynote_search_info = get_keynote_with_words_sets(keynote_df, FIREHYDRANT_SET)
    if keynote_search_info["status"] == "fail":
        fire_hydrant_info = {"status": "fail", 
                             "error message": "no keynote for FIRE HYDRANT"}
        # save the result
        with open(os.path.join(data_save_path, "fire_hydrant.json"), "w") as fp:
            json.dump(fire_hydrant_info, fp, indent=4)
        return None
    
    # a fire hydrant keynote exist
    detected_df = keynote_search_info["detected_df"]

    # search matches in the siteplan to find all fire hydrant
    # use the keynote clean image to do the match
    image = cv2.imread(os.path.join(img_save_path, "keynote_clean.png"))

    match_df, _, _, _ = single_keynote_match(
        image=image, 
        keynote_df=keynote_df, 
        index=list(detected_df.index)[0], 
        keynote_folder=keynote_folder, 
        display_image=display_image, 
        match_status_image=image)
    
    # draw the result image and save
    fire_hydrant_image = keynote_match_draw(
        detected_df=detected_df, 
        match_df=match_df, 
        image=display_image)
    cv2.imwrite(os.path.join(img_save_path, "fire_hydrant.png"), fire_hydrant_image)
    
    # summarize the total number of fire hydrant
    total_num_firehydrant = len(match_df)
    # save the results
    fire_hydrant_info = {"status": "succeed", 
                         "total_number": total_num_firehydrant, 
                         "keynote_index": list(detected_df.index)[0]}
    with open(os.path.join(data_save_path, "fire_hydrant.json"), "w") as fp:
        json.dump(fire_hydrant_info, fp, indent=4)
    match_df.to_csv(os.path.join(data_save_path, "fire_hydrant.csv"), index=False)

    # read in the cost estimate file
    ce_form = cost_estimate_load(orig_img_path)
    # update the information
    ce_form.quantity_update(
        sheet_name="onsite", 
        description="Fire Hydrant Assembly (includes GV)", 
        quantity=total_num_firehydrant, 
        input_unit="EA")
    

def fire_hydrant_post(
        orig_img_path: str = None):
    """
    Return results for fire hydrant task on siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load fire hydrant information
    with open(os.path.join(data_save_path, "fire_hydrant.json"), "r") as fp:
        fire_hydrant_info = json.load(fp)

    return fire_hydrant_info