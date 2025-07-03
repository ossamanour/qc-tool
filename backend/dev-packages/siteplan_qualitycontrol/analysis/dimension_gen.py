"""
Perform dimension module.
"""
import os
from pathlib import Path
import cv2
import json

from siteplan_qualitycontrol.utils import arrow_angle_read_csv
from siteplan_qualitycontrol.basic import arrow_pair_search, arrow_connect_search, connected_arrow_clean
from siteplan_qualitycontrol.basic import arrow_pair_draw


def dimension_generate(
        orig_img_path: str = None):
    """
    Detect dimension notation on the siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    # use the original image as display image
    display_image = cv2.imread(orig_img_path)

    # read in the arrow tip with angle
    arrow_tip_angle_df = arrow_angle_read_csv(os.path.join(data_save_path, "arrow_angle.csv"))
    # if no arrow tip detected, no dimension
    if len(arrow_tip_angle_df) == 0:
        dimension_info = {"status": "fail", 
                          "error message": "no arrows detected"}
        # save ther results
        with open(os.path.join(data_save_path, "dimension.json"), "w") as fp:
            json.dump(dimension_info, fp, indent=4)
        return None

    # find arrow pairs based on angle
    match_arrow_pairs = arrow_pair_search(arrow_tip_angle_df)
    # if no dimension is detected
    if len(match_arrow_pairs) == 0:
        dimension_info = {"status": "fail", 
                          "error message": "no dimension arrow pairs detected"}
        # save ther results
        with open(os.path.join(data_save_path, "dimension.json"), "w") as fp:
            json.dump(dimension_info, fp, indent=4)
        return None
    
    # check connection and get connected arrow pairs
    connected_arrow_pairs = arrow_connect_search(orig_img_path, arrow_tip_angle_df, match_arrow_pairs)
    # clean connected arrow pairs to delete repreated arrows
    connected_arrow_pairs_clean = connected_arrow_clean(arrow_tip_angle_df, connected_arrow_pairs)
    # if no dimension is detected
    if len(connected_arrow_pairs_clean) == 0:
        dimension_info = {"status": "fail", 
                          "error message": "no dimension arrow pairs detected"}
        # save the results
        with open(os.path.join(data_save_path, "dimension.json"), "w") as fp:
            json.dump(dimension_info, fp, indent=4)
        return None
    
    # draw the image and save the pair dictionary
    connected_arrow_pairs_image = arrow_pair_draw(connected_arrow_pairs_clean, 
                                                  arrow_tip_angle_df, 
                                                  display_image)
    cv2.imwrite(os.path.join(img_save_path, "dimension.png"), connected_arrow_pairs_image)

    dimension_info = {"status": "succeed", 
                      "dimension_number": len(connected_arrow_pairs_clean), 
                      "dimension_arrow_pairs": connected_arrow_pairs_clean}
    # save the results
    with open(os.path.join(data_save_path, "dimension.json"), "w") as fp:
        json.dump(dimension_info, fp, indent=4)


def dimension_generate_post(
        orig_img_path: str = None):
    """
    Return the dimension detection results of the siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load dimension generation information
    with open(os.path.join(data_save_path, "dimension.json"), "r") as fp:
        dimension_info = json.load(fp)

    return dimension_info
