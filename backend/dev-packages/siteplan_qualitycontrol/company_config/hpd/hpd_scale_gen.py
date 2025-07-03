"""
Functions to detect the scale information for HPD landscape.
"""
import os
import cv2
import pandas as pd
from pandas import DataFrame
from pathlib import Path
import numpy as np

from siteplan_qualitycontrol.company_config.hpd.hpd_landscape import hpd_landscape_template_call, sub_image_get
from siteplan_qualitycontrol.utils import contours_generate, approx_poly
from siteplan_qualitycontrol.basic import text_extract


def hpd_scale_sub_img_gen(
        image: np.array = None):
    """
    Generate sub-image containing scale information from HPD template.

    @param: image: array of the input HDP templte.

    @return: sub_img: sub-image containing scale information.
    @return: sub_img_contours: list of contours for the sub-image.
    """
    # generate the sub-image containing scale information from the template
    template, config = hpd_landscape_template_call()

    contours, _ = contours_generate(image, thresh=250)
    rect_contours = approx_poly(contours)

    sub_img, sub_img_contours = sub_image_get(image, rect_contours, config, "scale_ruler", threshold=0.5, get_full=False)

    return sub_img, sub_img_contours


def hpd_scale_number_get(
        sub_img: np.array = None):
    """
    Detect scale number from the input HPD landscape sidebar sub image.

    @param: sub_img: sub-image of the HPD landscape sidebar.

    @return: scale_numbers: scale number 
    @return: most_frequent_top: 
    """
    # do ocr on sub image
    data_df = text_extract(sub_img)
    # get all numbers in the data_df
    for i in range(len(data_df)):
        if not data_df.iloc[i]["text"].isdigit():
            data_df.iloc[i] = None
    data_df.dropna(inplace=True)

    # get the numbers that are on the same line
    loc_top_list = list(data_df.top)
    most_frequent_top = max(set(loc_top_list), key=loc_top_list.count)
    scale_numbers = data_df.loc[data_df["top"] == most_frequent_top]

    return scale_numbers, most_frequent_top


def hpd_scale_ruler_gen(
        sub_img: np.array = None, 
        most_frequent_top: float = None):
    """
    Detect the scale ruler bar.

    @param: sub_img: sub-image containing the scale ruler.
    @param: most_frequent_top: 

    @return: (x, y, w, h): location of the detected scale ruler.
    """
    # generate contours and get only the root ones
    contours, hierarchy = contours_generate(sub_img, thresh=250, type=cv2.THRESH_BINARY)

    parent_contours = []
    for i, contour in enumerate(contours):
        if hierarchy[0][i, -1] == -1:
            parent_contours.append(contour)
    
    # find the rectangle contour closest to the numbers (on top of it)
    distances = {}
    for i, contour in enumerate(parent_contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        d = y + h - most_frequent_top
        if d < 0:
            distances[i] = d

    closet_contour_idx = [i for i in distances.keys() if distances[i] == max(distances.values())]

    (x, y, w, h) = cv2.boundingRect(parent_contours[closet_contour_idx[0]])

    return (x, y, w, h)


def hpd_scale_generate(
        orig_img_path: str = None):
    """
    Detect the scale from the HPD landscape image.

    @param: orig_img_path: string of path the originla PNG image.

    @return: scale_info: JSON containing the scale information.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    # read the original image
    image = cv2.imread(orig_img_path)

    # get the sub image containing scale information
    sub_img, sub_img_contours = hpd_scale_sub_img_gen(image)

    # get the scale numbers
    scale_numbers, most_frequent_top = hpd_scale_number_get(sub_img)
    scale_number = int(scale_numbers.iloc[1]["text"])

    # get the scale ruler pixel number
    scale_rule_loc = hpd_scale_ruler_gen(sub_img, most_frequent_top)

    # calculate the pixel 
    x, y, w, h = scale_rule_loc
    pixel_number = w + 1

    scale_info = {"scale_loc": scale_rule_loc, 
                  "scale_number": scale_number, 
                  "pixel_number": pixel_number}
    
    return scale_info