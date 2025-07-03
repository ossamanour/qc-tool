"""
Functions of tools for arrow detection related.
"""
import os
import cv2
import numpy as np
import math
import pandas as pd
from pandas import DataFrame
from pathlib import Path

from siteplan_qualitycontrol.utils import draw_contours_from_df, distance


def image_preprocessing(
        image: np.array = None, 
        dila_k: int = 4, 
        erod_k: int = 2):
    """
    Image preprocessing including grayscale, threshold, dilate, erode.

    @param: image: numpy array containing image, BGR format.
    @dila_k: integer, kernal size for dilate.
    @erod_k: integer, kernal size for erode.

    @return: image_erode: image after all processing.
    """
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)[1]

    dilate_kernel = np.ones((dila_k, dila_k), np.uint8)
    image_dilate = cv2.dilate(image_thresh, dilate_kernel, iterations=1)

    erode_kernel = np.ones((erod_k, erod_k), np.uint8)
    image_erode = cv2.erode(image_dilate, erode_kernel, iterations=1)

    return image_erode


def arrow_tip_search(
        image: np.array = None, 
        template: np.array = None, 
        dila_k: int = 4, 
        erod_k: int = 2):
    """
    Given the image and an arrow template, search for all arrow tips.

    @param: qc_img_path: path to the image (already cleaned by mask out unnecessary informations).
    @param: arrow_template_path: path to the arrow tip template image.
    @dila_k: integer, kernal size for dilate.
    @erod_k: integer, kernal size for erode.

    @return: arrow_tip_df: [id, contour, match, heirarch] Data Frame containing contour and match information of detected arrow tips. 
    """
    # only clean based on area, corner count clean is not used 
    # since for too small traiangles, corner detection gets wrong very often
    # image = cv2.imread(qc_img_path)
    # template = cv2.imread(arrow_template_path)
    
    # preprocessing image
    image_gray = image_preprocessing(image, dila_k, erod_k)
    template_gray = image_preprocessing(template)

    # do matching
    template_contours, _ = cv2.findContours(template_gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    template_contour = template_contours[1]

    contours, heirarchy = cv2.findContours(image_gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    arrow_tip_df = DataFrame()
    for i, contour in enumerate(contours):
        match = cv2.matchShapes(template_contour, contour, 1, 0.0)
        # a large threshold is used for match score because the template is too small
        if match < 0.7:
            # contour_save = np.copy(contour)
            temp = {"id": i, "contour": contour, "match": match, "hierarchy": heirarchy[0][i, :]}
            arrow_tip_df = pd.concat([arrow_tip_df, DataFrame([temp])], ignore_index=True, sort=False)
    
    # clean the match contours based on area, eliminate too small or too large contours
    template_area = cv2.contourArea(template_contour)
    for i in range(len(arrow_tip_df)):
        contour = arrow_tip_df.iloc[i].contour
        contour_area = cv2.contourArea(contour)
        if 0.5*template_area > contour_area or contour_area > 1.5*template_area:
            arrow_tip_df.iloc[i] = None
    arrow_tip_df.dropna(inplace=True)
    arrow_tip_df.reset_index(drop=True, inplace=True)

    return arrow_tip_df


def arrow_tip_angle(
        arrow_tip_df: DataFrame = None):
    """
    Calculate the angle of all arrow tips, botton to tip.

    @param: arrow_tip_df: [id, contour, match, heirarch] Data Frame containing contour and match information of detected arrow tips. 

    @return: arrow_tip_angle_df: [id, contour, match, heirarch, angle, tip_pt, mid_pt] Data Fram containing information of all detected arrow tips.
    """
    # add columns to arrow_contours_df 
    arrow_tip_angle_df = DataFrame()
    for i in range(len(arrow_tip_df)):
        contour = arrow_tip_df.iloc[i].contour
        # for each contour, find the triangle
        area, tri_points = cv2.minEnclosingTriangle(contour)

        # exit cases in which the min enclosing triangle cannot be found
        if tri_points is not None:
            # calculate direction of the arrow
            (pt1, pt2, pt3) = tri_points.squeeze()
            d12 = distance(pt1, pt2)
            d13 = distance(pt1, pt3)
            d23 = distance(pt2, pt3)
            if min([d12, d13, d23]) == d12:
                ptc = (pt1+pt2) // 2
                pte = pt3
            elif min([d12, d13, d23]) == d13:
                ptc = (pt1+pt3) // 2
                pte = pt2
            else:
                ptc = (pt2+pt3) // 2
                pte = pt1
            angle = math.atan2((np.intp(pte[0])-np.intp(ptc[0])), (np.intp(pte[1])-np.intp(ptc[1])))
            angle = math.degrees(angle)

            arrow_tip_angle_df = pd.concat([arrow_tip_angle_df, pd.concat([DataFrame([arrow_tip_df.iloc[i]]).reset_index(drop=True), DataFrame([{"angle": angle, "tip_pt": pte, "mid_pt": ptc}])], axis=1)], ignore_index=True, sort=False)

    return arrow_tip_angle_df


def arrow_tip_draw(
        df: DataFrame = None, 
        display_image: np.array = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 2, 
        with_angle: bool = True):
    """
    Draw all detected arrow tips and mark the angle.

    @param: df: Data Fram containing information of all detected arrow tips.
    @param: display_image: numpy array containing image to draw arrow tips.
    @param: color: tuple of color, format BGR.
    @param: thickness: thickness for draw.
    @param: with_angle: boolean indicating if angle information is also marked, default as True.

    @return: arrow_draw_image: numpy array of image with all arrow tips draw.
    """
    display_image_return = display_image.copy()
    
    if with_angle:
        assert "angle" in df.keys(), "No angle information."
        # draw contours without index 
        arrow_draw_image = draw_contours_from_df(df, display_image_return, color, thickness, idx_mark=False)
        # mark angle
        for i in range(len(df)):
            contour = df.iloc[i].contour
            angle = df.iloc[i].angle
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.putText(arrow_draw_image, f"{i}-{str(round(angle, 2))}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness)
    else:
        # draw with no angle information, then draw contours with index
        arrow_draw_image = draw_contours_from_df(df, display_image_return, color, thickness, idx_mark=True)

    return arrow_draw_image


