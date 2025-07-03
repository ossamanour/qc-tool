"""
Functions of tools for parking task.
"""
import os
from pathlib import Path
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import cv2

from siteplan_qualitycontrol.utils import contours_generate, contour_outer_maskout
from siteplan_qualitycontrol.basic import string_loc_detect
from siteplan_qualitycontrol.images import image_number_read


def parking_count_legend_image_clean(
        parking_count_legend_image: np.array = None):
    """
    Clean up the parking count legend by removing the X inside it.

    @param: parking_count_legend_image: image of the parking count legend.

    @return: parking_count_legend_image: cleaned legend image.
    """
    contours, _ = contours_generate(image=parking_count_legend_image, type=cv2.THRESH_BINARY)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # mask out the X mark inside
    cv2.drawContours(parking_count_legend_image, [sorted_contours[2]], -1, (255, 255, 255), -1)
    return parking_count_legend_image


# def parking_count_legend_generate(
#         source_image: np.array = None, 
#         ocr_df: DataFrame = None):
#     # detect word "PARKING COUNT"
#     parking_count_legend_text = string_loc_detect(ocr_df, "PARKING COUNT")
#     # return None if there is no legend for parking count
#     if len(parking_count_legend_text) == 0:
#         parking_count_legend_text_loc = (-1, -1, -1, -1)
#         parking_count_legend_image_loc = (-1, -1, -1, -1)
#         parking_count_legend_image = None
#         return parking_count_legend_text_loc, parking_count_legend_image_loc, parking_count_legend_image
    
#     # generate the legend image
#     x, y, w, h, text, th = parking_count_legend_text.iloc[0]
#     parking_count_legend_text_loc = tuple(map(int, (x, y, w, h)))
#     # get the image patch
#     patch_start_x = x - 2 * w
#     patch_end_x = x - 5
#     patch_start_y = y - 2 * h
#     patch_end_y = y + 2 * h
#     image_patch = source_image[patch_start_y:patch_end_y, patch_start_x:patch_end_x, :]
#     # detect borders (only the external border)
#     gray = cv2.cvtColor(image_patch, cv2.COLOR_BGR2GRAY)
#     canny_edge = cv2.Canny(gray, 30, 200)
#     contours, _ = cv2.findContours(canny_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#     # make sure the legend image overlap with the legend text vertically
#     new_y = 2 * h
#     new_contours = []
#     for c in contours:
#         cx, cy, cw, ch = cv2.boundingRect(c)
#         if (cy >= new_y and cy <= (new_y+th)) or ((cy+ch) >= new_y and (cy+ch) <= (new_y+th)) or (cy < new_y and (cy+ch) > (new_y+th)):
#             new_contours.append(c)

#     # find the most left contour
#     sorted_contours = sorted(new_contours, key=lambda c: cv2.boundingRect(c)[0])
#     x, y, w, h = cv2.boundingRect(sorted_contours[-1])
#     x = x + patch_start_x
#     y = y + patch_start_y
#     parking_count_legend_image = source_image[y-4:y+h+4, x-4:x+w+4, :]
#     parking_count_legend_image_loc = tuple(map(int, (x, y, w, h)))

#     # clean the image
#     parking_count_legend_image = parking_count_legend_image_clean(parking_count_legend_image)

#     return parking_count_legend_text_loc, parking_count_legend_image_loc, parking_count_legend_image


def parking_count_search(
        source_image: np.array = None, 
        parking_count_legend_image: np.array = None, 
        parking_count_legend_image_loc: tuple = None, 
        tolerance: float = 0.25):
    """
    Detect parking count notation through matching on the legend.

    @param: source_image: array of image to be detected.
    @param: parking_count_legend_image: array of the parking count legend image.
    @param: parking_count_legend_image_loc: tuple containing location information of the parking count legend.
    @param: tolerance: tolerance for matching.

    @return: match_contours: list of contours of all detected matches. 
    @return: match_hierarchy: list of hierarchy of all detected matches.
    """
    # mask out the legend image
    (x, y, w, h) = parking_count_legend_image_loc
    # the copy step is to prevent the legend image from changing while masking out on the source image
    target = source_image.copy()
    target = cv2.rectangle(target, (x, y), (x+w, y+h), (255, 255, 255), -1)

    # do contour match
    template_contours, _ = contours_generate(parking_count_legend_image, type=cv2.THRESH_BINARY)
    sorted_template_contours = sorted(template_contours, key=cv2.contourArea, reverse=True)
    template_contour = sorted_template_contours[2]

    # find match on the target image
    target_contours, target_hierarchy = contours_generate(target, thresh=250, type=cv2.THRESH_BINARY)

    match_contours = []
    match_hierarchy = []
    index = 0
    for c in target_contours:
        match = cv2.matchShapes(template_contour, c, 1, 0.0)
        if match < 0.005:
            if np.abs(cv2.contourArea(c) - cv2.contourArea(template_contour)) / cv2.contourArea(template_contour) <= tolerance:
                # since we only want the inner edge of the parking count legend, remove the contours that has parent -1
                # if target_hierarchy[0, index, -1] != -1:
                match_contours.append(c)
                match_hierarchy.append(target_hierarchy[:, index, :])
        index = index + 1

    return match_contours, match_hierarchy


def parking_count_read(
        original_image: np.array = None, 
        match_contours: list = []):
    """
    Read the parking count number of the detected parking count notation.

    @param: original_image: array of the siteplan image.
    @param: match_contours: list of contours of detected parking count matches.

    @return: parking_count_df: dataframe containing results for parking count detection and read.
    """
    parking_count_df = DataFrame()
    source_image = original_image.copy()
    # loop through all match contours
    for contour in match_contours:
        # mask out everything outside the contour with color white
        masked_image = contour_outer_maskout(source_image, contour)
        # take out the sub image
        (x, y, w, h) = cv2.boundingRect(contour)
        sub_image = masked_image[y:y+h, x:x+w, :]
        # read the number
        number = image_number_read(sub_image)

        # save the results
        temp = {"contour": contour, "left": x, "top": y, "width": w, "height": h, "number": int(number)}
        parking_count_df = pd.concat([parking_count_df, DataFrame([temp])], ignore_index=True, sort=False)

    return parking_count_df


def parking_count_draw(
        parking_count_df: DataFrame = None, 
        display_image: np.array = None, 
        parking_count_legend_series: Series = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 2):
    """
    Boxed out the detected parking count and mark the number read from the siteplan.

    @param: parking_count_df: datafram containing results for parking count detection and read.
    @param: display_image: array of image to draw.
    @param: parking_count_legend_series: series containing information of the parking count legend.
    @param: color: tuple of color.
    @param: thickness: thickness for drawing.

    @return: display_image_return: image with detected parking count boxed out and number marked.
    """
    display_image_return = display_image.copy()

    # box out the parking count legend
    (name, image, tx, ty, tw, th, ix, iy, iw, ih) = parking_count_legend_series.iloc[0]
    cv2.rectangle(display_image_return, (tx, ty), (tx+tw, ty+th), color, thickness)
    cv2.rectangle(display_image_return, (ix, iy), (ix+iw, iy+ih), color, thickness)

    # box out all the parking count and mark the number
    for i in range(len(parking_count_df)):
        (contour, x, y, w, h, number) = parking_count_df.iloc[i]
        cv2.drawContours(display_image_return, [contour], -1, color, thickness)
        cv2.putText(display_image_return, str(number), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, color, thickness)

    return display_image_return
