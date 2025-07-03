"""
Function of tools for SEG template related.
"""
import os
import json
import cv2
import numpy as np

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.company_config.utils import sub_image_get, sub_image_mask_surround, sub_image_mask, contour_rect_mask_surround
from siteplan_qualitycontrol.basic import text_extract, block_extract, ocr_text_correction
from siteplan_qualitycontrol.utils import contours_generate, approx_poly, most_overlap_contour
from siteplan_qualitycontrol.company_config.utils import sub_image_get


def seg_siteplan_template_path():
    """
    Return the path to the SEG siteplan template.

    @return: path: absolute path to the SEG siteplan template image.
    """
    path = os.path.join(global_var.ROOT, "assets", "companies", "seg", "siteplan_template.png")
    return path


def seg_siteplan_template_call():
    """
    Call the SEG siteplan template.

    @return: template: array of the SEG siteplan template image.
    @return: config: config for the SEG siteplan template.
    """
    # read in template image
    path = os.path.join(global_var.ROOT, "assets", "companies", "seg", "siteplan_template.png")
    template = cv2.imread(path)
    # read in config file
    config_path = os.path.join(global_var.ROOT, "assets", "companies", "seg", "siteplan_config.json")
    with open(config_path, "r") as fp:
        config = json.load(fp)

    return template, config


def seg_siteplan_body_sidebar_generate(
        image: np.array = None):
    """
    Using the SEG siteplan template, seperate the siteplan image to main-body and sidebar.

    @param: image: array of the input siteplan image.

    @return: body_img: array of the main-body of the siteplan.
    @return: sidebar_img: array of the sidebar of the siteplan.
    """
    # get the template and config
    template, config = seg_siteplan_template_call()

    # generate contours
    contours, _ = contours_generate(image)
    rect_contours = approx_poly(contours)

    body_img, body_contour = sub_image_get(image, rect_contours, config, "main")
    sidebar_img, sidebar_contour = sub_image_get(image, rect_contours, config, "sidebar")

    return body_img, sidebar_img


def seg_siteplan_sidebar_info_generate(
        image: np.array = None):
    """
    Detect project information, including project title, address, from the input siteplan sidebar image.

    @param: image: input siteplan sidebar image.

    @return: information: JSON containing the detected prject information.
    """
    # get the template and config
    template, config = seg_siteplan_template_call()

    # generate contours
    contours, _ = contours_generate(image)
    rect_contours = approx_poly(contours)

    # get basic information
    # title
    title_img, title_contour = sub_image_get(image, rect_contours, config, "project_P", threshold=0.5, get_full=False)
    title_img = cv2.rotate(title_img, cv2.ROTATE_90_CLOCKWISE)
    # kernel = np.ones((3, 3), np.uint8)
    # title_img = cv2.erode(title_img, kernel)
    df = text_extract(title_img, custom_config=r'--oem 3 --psm 6')
    df = ocr_text_correction(title_img, df)
    title = " ".join(df["text"].iloc[1:])

    # address
    location_img, location_contour = sub_image_get(image, rect_contours, config, "location_P", threshold=0.5, get_full=False)
    location_img = cv2.rotate(location_img, cv2.ROTATE_90_CLOCKWISE)
    # kernel = np.ones((5, 5), np.uint8)
    # location_img = cv2.erode(location_img, kernel)
    # kernel = np.ones((2, 2), np.uint8)
    # location_img = cv2.dilate(location_img, kernel)
    # location_img = Image.fromarray(cv2.cvtColor(location_img, cv2.COLOR_BGR2RGB)).convert("L")

    df = text_extract(location_img, custom_config=r'--oem 3 --psm 6')
    df = ocr_text_correction(location_img, df)
    address = " ".join(df["text"].iloc[1:])
        
    # sheet_title_img, sheet_title_contour = sub_image_get(image, rect_contours, config, "sheet_title", threshold=0.5, get_full=False)

    # save the contour information to locate the info
    save_contours = {"title": title_contour.tolist(), 
                     "address": location_contour.tolist()}
    # generate information
    information = {"title": title, 
                   "address": address, 
                   "contours": save_contours}

    return information
    

    
