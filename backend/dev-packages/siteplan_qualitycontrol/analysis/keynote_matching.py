"""
Perform keynote match module.
"""
import os
from pathlib import Path
import cv2
import json
import pandas as pd

from siteplan_qualitycontrol.basic import keynote_match_prepare, keynote_initial_draw
from siteplan_qualitycontrol.basic import single_keynote_match


def keynote_match_pre(
        orig_img_path: str = None):
    """
    Prepare the siteplan image for keynote matching, including mask out keynote list.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # prepare the image for matching, including intial draw
    keynote_match_prepare(orig_img_path)
    # do the initial draw
    keynote_initial_draw(orig_img_path)


def keynote_match(
        orig_img_path: str = None, 
        index: int = None,
        match_threshold: float = 0.7):
    """
    Perform keynote match for one or all detected keynotes.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    @param: index: if None, detect all, if not, detect keynote [index]
    @param: match_threshold: threshold for matching algorithm.
    """
    # save folder
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    keynote_data_save_path = os.path.join(data_save_path, "keynote_match")
    keynote_img_save_path = os.path.join(img_save_path, "keynote_match")

    # read in the keynote data frame
    with open(os.path.join(data_save_path, "keynote.json"), "r") as fp:
        information = json.load(fp)
    keynote_df = pd.read_csv(os.path.join(information["key_folder"], "keynote.csv"))
    keynote_folder = information["key_folder"]

    # if no index is given, run matches for all keynotes without display update
    # use the clean-up image to do the match
    image = cv2.imread(os.path.join(img_save_path, "keynote_clean.png"))
    match_status_image = cv2.imread(os.path.join(img_save_path, "keynote_match_results.png"))
    if index is None:
        # empty dictionary to store the information of matching
        keynote_match_info = {}
        display_image = cv2.imread(orig_img_path)
        for index in range(len(keynote_df)):
            match_df, keynote_match_image, _, match_status_image = single_keynote_match(
                image=image, 
                keynote_df=keynote_df, 
                index=index, 
                keynote_folder=keynote_folder, 
                match_threshold=match_threshold, 
                display_image=display_image, 
                match_status_image=match_status_image
            )
            # for this part, only the the match_df and keynote_match_image is usable
            match_df.to_csv(os.path.join(keynote_data_save_path, f"keynote-{index+1}.csv"), index=False)
            cv2.imwrite(os.path.join(keynote_img_save_path, f"keynote-{index+1}.png"), keynote_match_image)
            if len(match_df) == 0:
                keynote_match_info[f"keynote-{index+1}"] = {
                    "status": "fail", 
                    "error message": "no match detected"}
            else:
                keynote_match_info[f"keynote-{index+1}"] = {
                    "status": "succeed", 
                    "match-number": len(match_df)}
        # save the keynote mactch information as json file
        with open(os.path.join(data_save_path, "keynote_match.json"), "w") as fp:
            json.dump(keynote_match_info, fp, indent=4)
    else:
        # if index is given, perform on on the given index
        match_df, keynote_match_image, single_match_status_image, match_status_image = single_keynote_match(
            image=image, 
                keynote_df=keynote_df, 
                index=index, 
                keynote_folder=keynote_folder, 
                match_threshold=match_threshold, 
                display_image=match_status_image, 
                match_status_image=match_status_image
        )
        # this is used for single cases
        match_df.to_csv(os.path.join(keynote_data_save_path, f"keynote-{index+1}.csv"), index=False)
        cv2.imwrite(os.path.join(keynote_img_save_path, f"keynote-{index+1}.png"), keynote_match_image)
        cv2.imwrite(os.path.join(img_save_path, "temp_keynote_match.png"), single_match_status_image)
        cv2.imwrite(os.path.join(img_save_path, "keynote_match_results.png"), match_status_image)
        # read the info first if file already exist
        if os.path.exists(os.path.join(data_save_path, "keynote_match.json")):
            with open(os.path.join(data_save_path, "keynote_match.json"), "r") as fp:
                keynote_match_info = json.load(fp)
        else:
            keynote_match_info = {}
        # update the information
        if len(match_df) == 0:
            keynote_match_info[f"keynote-{index+1}"] = {
                "status": "fail", 
                "error message": "no match detected"}
        else:
            keynote_match_info[f"keynote-{index+1}"] = {
                "status": "succeed", 
                "match-number": len(match_df)}
        # save the information
        with open(os.path.join(data_save_path, "keynote_match.json"), "w") as fp:
            json.dump(keynote_match_info, fp, indent=4)
    

def keynote_match_post(
        orig_img_path: str = None, 
        index: int = None):
    """
    Return results for keynote match on siteplan.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load keynote match information
    with open(os.path.join(data_save_path, "keynote_match.json"), "r") as fp:
        keynote_match_info = json.load(fp)
    
    if index is not None:
        return keynote_match_info[f"keynote-{index+1}"]
    else:
        return keynote_match_info

    



    