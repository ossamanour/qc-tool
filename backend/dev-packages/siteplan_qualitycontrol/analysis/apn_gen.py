"""
Script containing all functions to generate APN information from site plan.
"""

import os
import re
import cv2
import pandas as pd
from pandas import DataFrame
from pathlib import Path

from siteplan_qualitycontrol.basic import text_extract, ocr_draw, ocr_text_correction


def apn_text_detect(
        orig_img_path):
    """
    From the OCR analysis results, check if there is APN information on the site plan.

    @param: orig_img_path: path to the original image, PNG format.

    @return: apn_df: Data Frame containing all detected APN inforamtion, including location.
    """
    # use the data.csv to check if there is APN information on siteplan
    data_df = pd.read_csv(os.path.join(Path(orig_img_path).parent, "data", "data.csv"))
    apn_text_df = data_df[data_df.text.str.contains("APN", na=False)]

    # for each APN match, search if there is a APN number
    apn_df = DataFrame()
    image = cv2.imread(orig_img_path)
    for i in range(len(apn_text_df)):
        _, _, _, _, _, _, ax, ay, aw, ah, _, _ = apn_text_df.iloc[i]
        sub_image = image[ay-10:ay+ah+10, ax:]
        text_df = text_extract(sub_image)
        text_df = ocr_text_correction(sub_image, text_df)

        _, _, _, _, _, _, x, y, w, h, _, apn_text = text_df.iloc[text_df[text_df.text.str.contains("APN")].index[0]+1]
        apn_list = []
        tx = tw = 0
        # try different pattern
        patterns = [r"^[\d]{3}-[\d]{2}-[\d]{3}$", 
                    r"^[\d]{3}-[\d]{2}-[\d]{3}[A-Z]{1}$", 
                    r"^[\d]{8}$", 
                    r"^[\d]{8}[A-Z]{1}$", 
                    r"^[\d]{8}-[A-Z]{1}$"]
        for pattern in patterns:
            apn = re.findall(pattern, apn_text)
            if len(apn) != 0:
                tx = x
                tw = w
                apn_list = apn_list+apn

        new_x = ax
        new_y = ay-10
        new_w = tw+tx
        new_h = ah+20
        temp = {"left": new_x, "top": new_y, "width": new_w, "height": new_h, "APN": apn_list}
        apn_df = pd.concat([apn_df, DataFrame([temp])])

    return apn_df


def apn_generate(
        orig_img_path: str = None):
    """
    Given the path to the original image of the site plan page, generate APN information if exist.

    @param: orig_img_path: path to the original image, PNG format.

    @return: clean_apn_list: list containing all the detected APNs.
    """
    # save path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # detect all the apns
    apn_df = apn_text_detect(orig_img_path)

    # draw the image and save
    image = cv2.imread(orig_img_path)
    apn_detect_image = ocr_draw(apn_df, image)
    apn_df.to_csv(os.path.join(data_save_path, "apn.csv"), )
    cv2.imwrite(os.path.join(img_save_path, "apn.png"), apn_detect_image)

    # remove the duplicates and get the final APN
    if len(apn_df) == 0:
        clean_apn_list = []
    else:
        all_apns = sum(list(apn_df.APN.values), [])
        clean_apn_list = list(set(all_apns))

    return clean_apn_list

