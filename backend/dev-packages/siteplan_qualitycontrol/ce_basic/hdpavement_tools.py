"""
Functions of tools for heavy duty pavement detection.
"""
import os
import cv2
import pandas as pd
import numpy as np
from pandas import Series


def source_image_prepare(
        image: np.array = None):
    """
    Prepare siteplan image for heavy duty pavement detection.

    @param: image: array of main-body image of siteplan.

    @return: gray: prepared image.
    """
    # prepare the image by remove all the color part to avoid mis-detection
    B = image[:, :, 0].astype(np.float32)
    G = image[:, :, 1].astype(np.float32)
    R = image[:, :, 1].astype(np.float32)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # mask out where the three channels are different
    gray = np.where((B-G) == 0, gray, 255)
    gray = np.where((B-R) == 0, gray, 255)
    gray = np.where((G-R) == 0, gray, 255)

    return gray


def heavyduty_pavement_detect(
        source_image: np.array = None, 
        hd_pavement_legend_image: np.array = None, 
        hd_pavement_legend_image_loc: tuple = None, 
        tolerance: float = 0.05):
    """
    Detect heavy duty pavement on siteplan.

    @param: image: array of main-body image of siteplan.
    @param: hd_pavement_legend_image: array of image of heavy duty pavement legend.
    @param: hd_pavement_legend_image_loc: tuple containing location information of legend on the siteplan.
    @param: tolerance: tolerance for threshold for color matching.

    @return: clean_contours: list of contours of all detected areas.
    """
    # mask out the legend image
    (x, y, w, h) = hd_pavement_legend_image_loc
    target = source_image.copy()
    target = cv2.rectangle(target, (x, y), (x+w, y+h), (255, 255, 255), -1)
    # all heavy-duty pavement related jobs are performed on grayscale, this is based on the fact that the pavement is always marked with solid gray (might with different shade of gray)

    # prepare the image to grayscale
    # use grayscale instead of color image because it's faster
    gray = source_image_prepare(target)

    # get the hist of legend
    legend_image_gray = cv2.cvtColor(hd_pavement_legend_image, cv2.COLOR_BGR2GRAY)
    legend_hist = cv2.calcHist([legend_image_gray], [0], None, [256], [0, 256])
    # set intensity 0 and 255 to zero to avoid mis-detection
    legend_hist[0] = 0
    legend_hist[255] = 0
    # get intensity for pavement
    pavement_color = np.argmax(legend_hist)

    # use the tolerance to set threshold for color
    pavement_color_min = np.int64(np.floor(pavement_color * (1 - tolerance)))
    pavement_color_max = np.minimum(np.int64(np.floor(pavement_color * (1 + tolerance))), 254)

    # mask out all color but those in range (solid gray)
    mask = ~np.isin(gray, np.arange(pavement_color_min, pavement_color_max))
    gray[mask] = 255

    # find all external contours, and clean up the detected parts
    _, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # based on area, eliminate contours with too small area
    area_threshold = 50
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    keep_contours = []
    for c in sorted_contours:
        if cv2.contourArea(c) > area_threshold:
            keep_contours.append(c)
        else:
            break
    
    # based on if the contours has most of its content as white, usually for grids
    clean_contours = []
    p_list = []
    for c in keep_contours:
        area = cv2.contourArea(c)
        contour_mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.drawContours(contour_mask, [c], -1, 255, -1)
        gray_mask = gray == 255
        results = (np.logical_and(contour_mask, gray_mask)).sum()
        p = results / area
        p_list.append(p)
        if p <= 0.75:
            clean_contours.append(c)

    return clean_contours


def heavyduty_pavement_draw(
        contours: list = None, 
        display_image: np.array = None, 
        hd_pavement_legend_series: Series = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 2):
    """
    Mask out all detected heavy duty pavement area.

    @param: contours: list of all detected heavy duty pavement areas.
    @param: display_image: array of image to draw.
    @param: hd_pavement_legend_series: series containing information of heavy duty pavement legend.
    @param: color: tuple of color.
    @param: thickness: thickenss for drawing.

    @return: display_image_return: image with all detected heavy duty pavement area masked out.
    """
    display_image_return = display_image.copy()

    # box out the heavyduty pavement legend
    (name, image, tx, ty, tw, th, ix, iy, iw, ih) = hd_pavement_legend_series.iloc[0]
    cv2.rectangle(display_image_return, (tx, ty), (tx+tw, ty+th), color, thickness)
    cv2.rectangle(display_image_return, (ix, iy), (ix+iw, iy+ih), color, thickness)

    # mask out all the heavyduty pavement
    cv2.drawContours(display_image_return, contours, -1, color, -1)

    return display_image_return


def heavyduty_pavement_measure(
        orig_img_path: str = None, 
        contours: list = None, 
        scale_info: list = None):
    """
    Measure the area of detected heavy duty pavement.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    @param: contours: list of all detected heavy duty pavement areas.
    @param: scale_info: dictionary containing scale information.

    @return: area_in_sf: area in unit of square feet.
    """
    original_image = cv2.imread(orig_img_path)
    # calculate the area in pixel
    mask = np.zeros(original_image.shape[:2])
    cv2.drawContours(mask, contours, -1, 1, -1)
    area_in_pixel = mask.sum()

    # use the scale ruler to get the are in SF
    feet_pixel = scale_info["pixel_number"] / scale_info["scale_number"]
    square_feet = feet_pixel ** 2

    area_in_sf = area_in_pixel / square_feet

    return area_in_sf
