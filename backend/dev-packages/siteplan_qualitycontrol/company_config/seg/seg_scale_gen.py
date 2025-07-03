"""
Functions to detect the scale information for SEG siteplan.
"""
import os
from pathlib import Path
import cv2
import json
import numpy as np
import pandas as pd
from pandas import DataFrame
import re

from siteplan_qualitycontrol.utils import rectangle_contour_search, get_closest_contour
from siteplan_qualitycontrol.basic import string_loc_detect, text_extract


def seg_scale_ruler_bar_generate(
        image: np.array = None):
    """
    Detect scale ruler bar on the given SEG siteplan image.

    @param: image: array of the input SEG siteplan image.

    @return: (x, y, w, h): location for the detected ruler, return None if nothing is detected.
    """
    # since the thresh image is needed, use separate pre-processing
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image_thresh = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY_INV)

    # search all the contours
    contours, heirarchy_all = cv2.findContours(image_thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # get id for all rectangle contours
    rectangle_id_list = rectangle_contour_search(contours, epsilon_ratio=0.01)

    # based on the heirarchy, find the parent-chilren pairs
    parent_chilren_dict = {}
    for i in rectangle_id_list:
        hierarchy = heirarchy_all[0][i, :]
    # for i in range(len(rectangle_contour_df)):
        # (id, contour, hierarchy, approx) = rectangle_contour_df.iloc[i]
        if hierarchy[-1] == -1:
            # if parent is none, it is a parent
            parent_chilren_dict[i] = []
        elif hierarchy[-1] not in parent_chilren_dict.keys():
            # not in the key list yet, add the pair
            parent_chilren_dict[hierarchy[-1]] = [i]
        else:
            # parent already in the key list, add child 
            parent_chilren_dict[hierarchy[-1]].append(i)

    # clean up the detected parent-children pair based on
    # 1. number of children [>1]
    # 2. area of children compared to parent [40%~60%]
    temp_dict = {}
    for parent, children in parent_chilren_dict.items():
        # parent_idx = np.where(rectangle_contour_df.id == parent)[0][0]
        # parent_contour = rectangle_contour_df.iloc[parent_idx].contour
        parent_contour = contours[parent]
        if len(children) > 1:
            # threshhold set to 1 instead of 0 to eliminate false detection of the inner and border edges of a shape.
            parent_area = cv2.contourArea(parent_contour)
            total_children_area = 0
            # calculate all chidren areas
            for child in children:
                # child_idx = np.where(rectangle_contour_df.id == child)[0][0]
                # child_contour = rectangle_contour_df.iloc[child_idx].contour
                child_contour = contours[child]
                area = cv2.contourArea(child_contour)
                total_children_area = total_children_area + area
            # compare area
            if total_children_area/parent_area >= 0.4 and total_children_area/parent_area <= 0.6:
                temp_dict[parent] = children

    # further clean the parent-children pair based on detection of the black blocks 
    # this makes the black/white area close to 50%
    parent_children_clean_dict = {}
    for parent, children in temp_dict.items():
        # parent_idx = np.where(rectangle_contour_df.id == parent)[0][0]
        # parent_approx = rectangle_contour_df.iloc[parent_idx].approx
        parent_contour = contours[parent]
        eps = 0.01 * cv2.arcLength(parent_contour, True)
        parent_approx = cv2.approxPolyDP(parent_contour, eps, True)
        (x, y, w, h) = cv2.boundingRect(parent_approx)
        
        parent_image = image_thresh[y:y+h, x:x+w]
        hist = cv2.calcHist([parent_image], [0], None, [256], [0, 256])
        # check percentage of the black pixels
        if hist[0]/hist.sum() >= 0.4 and hist[0]/hist.sum() <=0.6:
            parent_children_clean_dict[parent] = children

    if len(parent_children_clean_dict) != 1:
        return None
    else:
        (x, y, w, h) = cv2.boundingRect(contours[list(parent_children_clean_dict.keys())[0]])

        return x, y, w, h 


def seg_scale_number_gen(
        scale_ruler_loc: tuple = None, 
        data_df: DataFrame = None, 
        image: np.array = None):
    """
    Given the location information of scale ruler, find the scale of the site plan.

    @param: scale_ruler_loc: (x, y, w, h), location information of the scale ruler.
    @param: data_df: data frame containing OCR analysis on the site plan.
    @param: image: numpy image of the site plan image, format PNG.

    @return: scale: detected scale.
    """
    # search the word "SCALE"
    scale_text_df = string_loc_detect(data_df, detect_string="SCALE")
    # find the one closet to the scale ruler bar
    scale_text_loc = get_closest_contour(scale_ruler_loc, scale_text_df)

    # use ocr text detection to get the measure scale
    (sx, sy, sw, sh) = scale_ruler_loc
    (x, y, w, h) = scale_text_loc
    
    sub_image = image[y-h//2:y+3*h//2, x:sx+sw]
    # clean up image before text detection: remove some gray lines 
    sub_image[sub_image>127] = 255
    data_df = text_extract(sub_image)

    number_list = []
    for i in range(len(data_df)):
        text = data_df.iloc[i].text
        num = [int(s) for s in re.findall(r'\d+', text) if int(s) != 1]
        number_list = number_list + num

    scale = number_list[0]

    return scale


def seg_scale_generate(
        orig_img_path: str = None):
    """
    Detect scale information on the input SEG siteplan image.

    @param: image: array of input SEG siteplan image.

    @return: scale_info: JSON containing information of the detected scale.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    # use the original image as display image
    display_image = cv2.imread(orig_img_path)

    # use the body image to detect for scale ruler
    image = cv2.imread(os.path.join(img_save_path, "body.png"))
    
    # detect the scalr bar (black and white blocks)
    scale_ruler_loc = seg_scale_ruler_bar_generate(image)

    # detect the scale number
    data_df = pd.read_csv(os.path.join(data_save_path, "data.csv"))
    scale = seg_scale_number_gen(scale_ruler_loc, data_df, image)

    # calculate the pixel - scale number to have the ruler
    x, y, w, h = scale_ruler_loc
    pixel_number = (w + 1) / 3

    scale_info = {"scale_loc": scale_ruler_loc, 
                  "scale_number": scale, 
                  "pixel_number": pixel_number}

    return scale_info