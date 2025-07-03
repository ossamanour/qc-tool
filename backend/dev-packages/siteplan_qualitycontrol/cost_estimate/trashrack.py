"""
Functions for trash rack cost estimate task.
"""
import os
from pathlib import Path
import cv2
import json

from siteplan_qualitycontrol.ce_basic import get_keynote_with_words_sets, keynote_match_draw
from siteplan_qualitycontrol.ce_basic import TRASH_SET
from siteplan_qualitycontrol.basic import single_keynote_match
from siteplan_qualitycontrol.utils import keynote_read_csv
from siteplan_qualitycontrol.cost_estimate import cost_estimate_load


def trash_rack(
        orig_img_path: str = None):
    """
    Detect trash rack for cost estimate on siteplan image.

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

    # detect if there is a kynote for 'trash'
    keynote_search_info = get_keynote_with_words_sets(keynote_df, TRASH_SET)
    if keynote_search_info['status'] == "fail":
        trash_rack_info = {"status": "fail", 
                         "error message": "no keynote for TRASH RACK"}
        # save the results
        with open(os.path.join(data_save_path, "trash_rack.json"), "w") as fp:
            json.dump(trash_rack_info, fp, indent=4)
        return None
    
    # trash rack keynote exists
    detected_df = keynote_search_info["detected_df"]

    # search matches in the siteplan to find all trash racks
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
    trash_rack_image = keynote_match_draw(
        detected_df=detected_df, 
        match_df=match_df, 
        image=display_image)
    cv2.imwrite(os.path.join(img_save_path, "trash_rack.png"), trash_rack_image)

    # summarize the total number of trash rack
    total_num_trashrack = len(match_df)
    # save the results 
    trash_rack_info = {"status": "succeed", 
                       'total_number': total_num_trashrack, 
                       'keynote_index': list(detected_df.index)[0]}
    with open(os.path.join(data_save_path, "trash_rack.json"), "w") as fp:
        json.dump(trash_rack_info, fp, indent=4)
    match_df.to_csv(os.path.join(data_save_path, "trash_rack.csv"), index=False)

    # read in the cost estimate file
    ce_form = cost_estimate_load(orig_img_path)
    # update the information
    ce_form.quantity_update(
        sheet_name="onsite", 
        description="Bubble-up inlet w/ trash rack", 
        quantity=total_num_trashrack, 
        input_unit="EA")


def trash_rack_post(
        orig_img_path: str = None):
    """
    Return results for trash rack task on the given siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load light pole hydrant information
    with open(os.path.join(data_save_path, "trash_rack.json"), "r") as fp:
        trash_rack_info = json.load(fp)

    return trash_rack_info
