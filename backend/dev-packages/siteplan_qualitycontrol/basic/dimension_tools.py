"""
Functions of tools for dimension task.
"""
import os
from pathlib import Path
import pandas as pd 
from pandas import DataFrame
import cv2
import numpy as np
import json
import math

from siteplan_qualitycontrol.utils import contour_connection_check, distance


def arrow_pair_search(
        arrow_tip_angle_df: DataFrame = None, 
        angle_bias: float = 2.5, 
        line_angle_bias: float = 1.5):
    """
    Based on the detected arrow tips (with angle information), match them as pairs which consist of dimension notation based on angle information.

    @param: arrow_tip_angle_df: Data Frame containing contour, location information and angle of all detected arrow tips.
    @param: angle_bias: bias to control the arrow tip match.
    @param: line_angle_bias: bias to control the dimension line match.

    @return: match_arrow_pairs: dictionary in which each (key, val) pair is index of a match arrow tips.
    """
    # divide arrows based angles
    pos_angle_idx = arrow_tip_angle_df[0 < arrow_tip_angle_df.angle].index
    neg_angle_idx = arrow_tip_angle_df[0 >= arrow_tip_angle_df.angle].index
    neg_angle_idx = arrow_tip_angle_df.index

    # go through arrows with angle (0, 180]
    match_arrow_pairs = {}
    for idx1 in pos_angle_idx:
        tip_pt1 = np.array(arrow_tip_angle_df.iloc[idx1].tip_pt)
        mid_pt1 = np.array(arrow_tip_angle_df.iloc[idx1].mid_pt)
        angle1 = arrow_tip_angle_df.iloc[idx1].angle
        paired_arrows = []
        for idx2 in neg_angle_idx:
            tip_pt2 = np.array(arrow_tip_angle_df.iloc[idx2].tip_pt)
            mid_pt2 = np.array(arrow_tip_angle_df.iloc[idx2].mid_pt)
            angle2 = arrow_tip_angle_df.iloc[idx2].angle
            # not using exact 180 degree, give a tolerance of +-1.5 degree
            if ((180-angle_bias) <= np.abs(angle1-angle2)) and (np.abs(angle1-angle2) <= (180+angle_bias)):
                # check the line direction to determine if they can be a pair
                line_angle = math.degrees(math.atan2((np.intp(mid_pt1[0])-np.intp(mid_pt2[0])), (np.intp(mid_pt1[1])-np.intp(mid_pt2[1]))))
                if np.abs(line_angle - angle1) <= line_angle_bias:
                    paired_arrows.append(idx2)
        if len(paired_arrows) > 0:
            match_arrow_pairs[idx1] = paired_arrows

    return match_arrow_pairs


def arrow_connect_search(
        img_path: str = None, 
        arrow_tip_angle_df: DataFrame = None, 
        match_arrow_pairs: dict = None):
    """
    Further clean up the match arrow tips by checking if the two arrow tips are connected.

    @param: img_path: path to the site plan image.
    @param: arrow_tip_angle_df: Data Frame containing contour, location information and angle of all detected arrow tips.
    @param: match_arrow_pair: dictionary in which each (key, val) pair is index of a match arrow tips.

    @return: connected_arrow_pairs: dictionary in which each (key, val) pair is index of a connected match arrow tips.
    """
    image = cv2.imread(img_path)

    # check if arrows in each pair are connected
    connected_arrow_pairs = {}
    for idx1 in match_arrow_pairs.keys():
        paired_arrows = match_arrow_pairs[idx1]
        connected_arrows = []
        # go through all paired arrows
        for idx2 in paired_arrows:
            contour1 = np.array(arrow_tip_angle_df.iloc[idx1].contour)
            contour2 = np.array(arrow_tip_angle_df.iloc[idx2].contour)
            connection = contour_connection_check(contour1, contour2, image)
            if connection:
                connected_arrows.append(idx2)
        if len(connected_arrows) == 1:
            # if only found 1 pair, keep it
            connected_arrow_pairs[idx1] = connected_arrows[0]
        if len(connected_arrows) > 1:
            # if multiple pair matches, keep the closest
            distances = []
            for idx2 in connected_arrows:
                pt1 = np.array(arrow_tip_angle_df.iloc[idx1].mid_pt)
                pt2 = np.array(arrow_tip_angle_df.iloc[idx2].mid_pt)
                distances.append(distance(pt1, pt2))
            connected_arrow_pairs[idx1] = connected_arrows[np.array(distances).argmin()]

    return connected_arrow_pairs


def connected_arrow_clean(
        arrow_tip_angle_df: DataFrame = None, 
        connected_arrow_pairs: dict = None):
    """
    Clean the detected connected arrow tip pair.

    @param: arrow_tip_angle_df: Data Frame containing contour, location information and angle of all detected arrow tips.
    @param: connected_arrow_pairs: dictionary in which each (key, val) pair is index of a connected match arrow tips.

    @return: connected_arrow_pairs_clean: dictionary in which each (key, val) pair is index of a connected match arrow tips.
    """
    # duplicates, this happens because some of the arrow tips are not detected.
    repeat_dict = {}
    for key, val in connected_arrow_pairs.items():
        if val not in repeat_dict.keys():
            repeat_dict[val] = [key]
        else:
            repeat_dict[val].append(key)
    repeated_tips = [key for key, val in repeat_dict.items() if len(val) > 1]

    connected_arrow_pairs_clean = connected_arrow_pairs.copy()
    # calculate distacne and keep on the closest pair
    for i in range(len(repeated_tips)):
        idx1 = repeated_tips[i]
        mid_pt1 = np.array(arrow_tip_angle_df.iloc[idx1].mid_pt)
        values = repeat_dict[idx1]
        distances = {}
        for j in range(len(values)):
            idx2 = values[j]
            mid_pt2 = np.array(arrow_tip_angle_df.iloc[idx2].mid_pt)
            d = distance(mid_pt1, mid_pt2)
            distances[idx2] = d
        # delete other tips but the closest pari
        del_list = [key for key, val in distances.items() if key != min(distances, key=distances.get)]
        connected_arrow_pairs_clean = {key:val for key, val in connected_arrow_pairs_clean.items() if key not in del_list}

    return connected_arrow_pairs_clean

def arrow_pair_draw(
        connected_arrow_pairs: dict = None, 
        arrow_tip_angle_df: DataFrame = None, 
        display_image: np.array = None):
    """
    Draw the detected connected arrow pairs and the dimension line on the site plan image.

    @param: connected_arrow_pairs: dictionary in which each (key, val) pair is index of a connected match arrow tips.
    @param: arrow_degree_df_path: path to the csv file for the Data Frame of detected arrow tips with angle information.
    @param: display_image: numpy array containing the image to draw.

    @return: display_image_return: numpy array containing image with the arrow pairs and dimensino line draw.
    """
    # copy image
    display_image_return = display_image.copy()
    # draw the arrow pairs
    for idx1 in connected_arrow_pairs.keys():
        idx2 = connected_arrow_pairs[idx1]
        contour1 = np.array(arrow_tip_angle_df.iloc[idx1].contour)
        contour2 = np.array(arrow_tip_angle_df.iloc[idx2].contour) 
        cv2.drawContours(display_image_return, [contour1], -1, (255, 0, 255), 2)
        cv2.drawContours(display_image_return, [contour2], -1, (255, 0, 255), 2)
        pt1 = np.intp(np.array(arrow_tip_angle_df.iloc[idx1].mid_pt))
        pt2 = np.intp(np.array(arrow_tip_angle_df.iloc[idx2].mid_pt))
        cv2.line(display_image_return, pt1, pt2, (255, 0, 255), 2)

    return display_image_return