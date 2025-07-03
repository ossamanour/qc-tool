"""
Function for ADA sign cost estimate task.
"""
import os
from pathlib import Path
import cv2
import json

from siteplan_qualitycontrol.ce_basic import get_keynote_with_words_sets, keynote_match_draw
from siteplan_qualitycontrol.ce_basic import ADASIGN_SET
from siteplan_qualitycontrol.basic import single_keynote_match
from siteplan_qualitycontrol.utils import keynote_read_csv
from siteplan_qualitycontrol.cost_estimate import cost_estimate_load


def ada_sign(
        orig_img_path: str = None):
    """
    Detect ADA sign for cost estimate on siteplan image.

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

    # detect if there is a keynote for 'ada sign', this corresponding to ada space
    keynote_search_info = get_keynote_with_words_sets(keynote_df, ADASIGN_SET)
    if keynote_search_info['status'] == "fail":
        ada_sign_info = {"status": "fail", 
                         "error message": "no keynote for ADA AIGN"}
        # save the results
        with open(os.path.join(data_save_path, "ada_sign.json"), "w") as fp:
            json.dump(ada_sign_info, fp, indent=4)
        return None
    
    # ada sign keynote exists
    detected_df = keynote_search_info["detected_df"]

    # search matches in the siteplan to find all ada sign
    # use the keynote clean image to do match
    image = cv2.imread(os.path.join(img_save_path, "keynote_clean.png"))

    match_df, _, _, _ = single_keynote_match(
        image=image, 
        keynote_df=keynote_df, 
        index=list(detected_df.index)[0], 
        keynote_folder=keynote_folder, 
        display_image=display_image, 
        match_status_image=image)

    # draw the result image and save
    ada_sign_image = keynote_match_draw(
        detected_df=detected_df, 
        match_df=match_df, 
        image=display_image)
    cv2.imwrite(os.path.join(img_save_path, "ada_sign.png"), ada_sign_image)

    # summarize the total number of ada sign
    total_num_adasign = len(match_df)
    # save the results
    ada_sign_info = {"status": "succeed", 
                     "total_number": total_num_adasign, 
                     "keynote_index": list(detected_df.index)[0]}
    with open(os.path.join(data_save_path, "ada_sign.json"), "w") as fp:
        json.dump(ada_sign_info, fp, indent=4)
    match_df.to_csv(os.path.join(data_save_path, "ada_sign.csv"), index=False)

    # read in the cost estimate file
    ce_form = cost_estimate_load(orig_img_path)
    # update the information
    ce_form.quantity_update(
        sheet_name="onsite", 
        description="ADA space", 
        quantity=total_num_adasign, 
        input_unit="EA")
    

def ada_sign_post(
        orig_img_path: str = None):
    """
    Return results for ADA sign task on siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load light pole hydrant information
    with open(os.path.join(data_save_path, "ada_sign.json"), "r") as fp:
        ada_sign_info = json.load(fp)

    return ada_sign_info


