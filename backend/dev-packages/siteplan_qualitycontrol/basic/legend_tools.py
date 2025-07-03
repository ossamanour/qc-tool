"""
Functions of tools for lengend related.
"""
import os
import cv2
import pandas as pd
import numpy as np
from pandas import DataFrame

from siteplan_qualitycontrol.basic import string_loc_detect


def detect_legend(
        legend_name: str = None, 
        source_image: np.array = None, 
        ocr_df: DataFrame = None):
    """
    Detect legend by name.

    @param: legend_name: legend name.
    @param: source_image: array of siteplan image.
    @param: ocr_df: dataframe containing OCR results on the source image.

    @return: legend_text_loc: location information of legend text.
    @return: legend_image_loc: location information of legend image. 
    @return: legend_image: array of detected legend image.
    """
    # detect the legend name from ocr results (use paragraph.csv)
    legend_text = string_loc_detect(ocr_df, legend_name)
    # return None if there is no legend name detected
    if len(legend_text) == 0:
        legend_text_loc = (-1, -1, -1, -1)
        legend_image_loc = (-1, -1, -1, -1)
        legend_image = None
        return legend_text_loc, legend_image_loc, legend_image
    
    # generate the lgend image
    x, y, w, h, text, th = legend_text.iloc[0]
    legend_text_loc = tuple(map(int, (x, y, w, h)))
    # get the image patch
    patch_start_x = x - 2 * w
    patch_end_x = x - 5
    patch_start_y = y - 2 * h
    patch_end_y = y + 2 * h
    image_patch = source_image[patch_start_y:patch_end_y, patch_start_x:patch_end_x, :]
    # detect borders (only the external border)
    gray = cv2.cvtColor(image_patch, cv2.COLOR_BGR2GRAY)
    canny_edge = cv2.Canny(gray, 30, 200)
    contours, _ = cv2.findContours(canny_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # make sure the legend image overlap with the legend text vertically
    new_y = 2 * h
    new_contours = []
    for c in contours:
        cx, cy, cw, ch = cv2.boundingRect(c)
        if (cy >= new_y and cy <= (new_y+th)) or ((cy+ch) >= new_y and (cy+ch) <= (new_y+th)) or (cy < new_y and (cy+ch) > (new_y+th)):
            new_contours.append(c)

    # find the most left contour
    sorted_contours = sorted(new_contours, key=lambda c: cv2.boundingRect(c)[0])
    x, y, w, h = cv2.boundingRect(sorted_contours[-1])
    x = x + patch_start_x
    y = y + patch_start_y
    legend_image = source_image[y-4:y+h+4, x-4:x+w+4, :]
    legend_image_loc = tuple(map(int, (x, y, w, h)))

    return legend_text_loc, legend_image_loc, legend_image



def save_legend(
        legend_name: str = None, 
        legend_text_loc: tuple = None,
        legend_image_loc: tuple = None, 
        legend_image: np.array = None, 
        data_save_path: str = None):
    """
    Save the legend information and legend image.

    @param: legend_name: legend name.
    @param: legend_text_loc: tuple of location information for legend text, (x, y, w, h).
    @param: legend_image_loc: tuple of location information for legend image, (x, y, w, h).
    @param: legend_image: array of legend image, format BGR.
    @param: data_save_path: path to the folder where all data/results data are saved.
    """
    # create legend save path if not exit
    legend_save_path = os.path.join(data_save_path, "legends")
    os.makedirs(legend_save_path, exist_ok=True)
    
    # check if there is already a data frame csv file
    legend_df_path = os.path.join(legend_save_path, "legend.csv")
    if os.path.exists(legend_df_path):
        legend_df = pd.read_csv(legend_df_path)
        # if legend already exist, jump out
        if legend_name in legend_df.name.values:
            return
    else:
        legend_df = DataFrame()

    # save the image and the information
    cv2.imwrite(os.path.join(legend_save_path, f"{legend_name}.png"), legend_image)
    temp = {"name": legend_name, 
            "image": f"{legend_name}.csv",
            "legend_text_left": legend_text_loc[0], 
            "legend_text_top": legend_text_loc[1],
            "legend_text_width": legend_text_loc[2],
            "legend_text_height": legend_text_loc[3],
            "legend_imag_left": legend_image_loc[0],
            "legend_imag_top": legend_image_loc[1],
            "legend_imag_width": legend_image_loc[2],
            "legend_imag_height": legend_image_loc[3],}
    legend_df = pd.concat([legend_df, DataFrame([temp])], ignore_index=True, sort=False)
    legend_df.to_csv(legend_df_path, index=False)

    return


def select_legend(legend_name: str = None, 
                  data_save_path: str = None):
    """
    Select legend by name from the saved detected legend csv.

    @param: legend_name: legend name.
    @param: data_save_path: path to the folder where all data/results data are saved.

    @return: series containing legend information.
    """
    legend_df_path = os.path.join(data_save_path, "legends", "legend.csv")
    legend_df = pd.read_csv(legend_df_path)
    return legend_df.loc[legend_df["name"] == legend_name]