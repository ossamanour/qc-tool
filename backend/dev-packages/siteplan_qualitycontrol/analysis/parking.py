"""
Perform parking count module.
"""
import os
from pathlib import Path
import cv2
import pandas as pd
import json
import numpy as np

from siteplan_qualitycontrol.basic import parking_count_search, parking_count_read, parking_count_draw
from siteplan_qualitycontrol.basic import save_legend, select_legend
from siteplan_qualitycontrol.basic import detect_legend, parking_count_legend_image_clean


def parking_count(
        orig_img_path: str = None):
    """
    Detect parking and count on the siteplan.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    display_image = cv2.imread(orig_img_path)

    # do all parking count detect on the body image
    body_image = cv2.imread(os.path.join(img_save_path, "body.png"))

    # find the parking count legend
    paragraph_df = pd.read_csv(os.path.join(data_save_path, "paragraph.csv"))
    # legend_text_loc, legend_image_loc, legend_image = parking_count_legend_generate(body_image, paragraph_df)
    legend_text_loc, legend_image_loc, legend_image = detect_legend(legend_name="PARKING COUNT", 
                                                                    source_image=body_image, 
                                                                    ocr_df=paragraph_df)
    # to cases with no parking count legend detected
    if legend_image is None:
        parking_count_info = {"status": "fail", 
                              "error message": "no parking count legend detected"}
        # save the results
        with open(os.path.join(data_save_path, "parking_count.json"), "w") as fp:
            json.dump(parking_count_info, fp, indent=4)
        return None
    
    # clean up the image
    legend_image = parking_count_legend_image_clean(legend_image)

    # save the parking count legend
    save_legend(legend_name="parking_count", 
                legend_text_loc=legend_text_loc, 
                legend_image_loc=legend_image_loc, 
                legend_image=legend_image, 
                data_save_path=data_save_path)
    
    # parking count search
    match_contours, match_hierarchy = parking_count_search(body_image, legend_image, legend_image_loc)

    # read the parking count number
    parking_count_df = parking_count_read(body_image, match_contours)
    parking_count_df.to_csv(os.path.join(data_save_path, "parking_count.csv"), index=False)

    # draw the image
    # read the legend
    parking_count_legend_series = select_legend(legend_name="parking_count", data_save_path=data_save_path)
    parking_count_image = parking_count_draw(parking_count_df, display_image, parking_count_legend_series)
    cv2.imwrite(os.path.join(img_save_path, "parking_count.png"), parking_count_image)

    total_parking = int(parking_count_df.number.values.sum())
    parking_count_info = {"status": "succeed", 
                          "total_parking": total_parking}
    
    # save the results
    with open(os.path.join(data_save_path, "parking_count.json"), "w") as fp:
        json.dump(parking_count_info, fp, indent=4)


def parking_count_post(
        orig_img_path: str = None):
    """
    Return the parking count detections results of sitelplan.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load parking count informaiton
    with open(os.path.join(data_save_path, "parking_count.json"), "r") as fp:
        parking_count_info = json.load(fp)
    
    return parking_count_info