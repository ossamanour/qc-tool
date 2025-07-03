"""
Functions of tools for HPD template related.
"""
import os
import json
import cv2
import numpy as np

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.company_config.utils import sub_image_get, sub_image_mask_surround, sub_image_mask
from siteplan_qualitycontrol.utils import contours_generate, approx_poly
from siteplan_qualitycontrol.basic import text_extract, block_extract, ocr_text_correction


def hpd_landscape_template_path():
    """
    Return the path to the HPD landscape template.

    @return: path: absolute path to the HPD landscape template.
    """
    path = os.path.join(global_var.ROOT, "assets", "companies", "hpd", "landscape_template.png")
    return path


def hpd_landscape_template_call():
    """
    Call the HPD landscape tempalte.

    @return: template: array of the HPD landscape template image.
    @return: config: config for the HPD landscape template.
    """
    # read in template image
    path = os.path.join(global_var.ROOT, "assets", "companies", "hpd", "landscape_template.png")
    template = cv2.imread(path)
    # read in config file
    config_path = os.path.join(global_var.ROOT, "assets", "companies", "hpd", "landscape_config.json")
    with open(config_path, "r") as fp:
        config = json.load(fp)

    return template, config


def hpd_landscape_body_sidebar_generate(
        image: np.array = None):
    """
    Using the HDP landscape template, seperate the landscape image into main-body and sidebar.

    @param: image: array of the input landscape image.

    @return: body_img: array of the main-body of the landscape.
    @return: sidebar_img: array of the sidebar of the landscape.
    """
    # get the template and config
    template, config = hpd_landscape_template_call()

    # generate contours
    contours, _ = contours_generate(image, thresh=250)
    rect_contours = approx_poly(contours)

    body_img, body_contour = sub_image_get(image, rect_contours, config, "main")
    sidebar_img, sidebar_contour = sub_image_get(image, rect_contours, config, "sidebar")

    # mask out the sidebar
    (x, y, w, h) = cv2.boundingRect(sidebar_contour)
    body_img[y:y+h, x:x+w, :] = 255

    return body_img, sidebar_img


def hpd_landscape_sidebar_info_generate(
        image: np.array = None):
    """
    Detect project information, including project title, address, from the input landscape sidebar image.

    @param: image: input landscape sidebar image.

    @return: information: JSON containing the detected prject information.
    """
    # get the template and config
    template, config = hpd_landscape_template_call()

    # generate contours
    contours, _ = contours_generate(image, thresh=250)
    rect_contours = approx_poly(contours)

    # get basic information
    sub_img, sub_img_contours = sub_image_get(image, rect_contours, config, "project_address_P", threshold=0.5, get_full=False)
    sub_img = cv2.rotate(sub_img, cv2.ROTATE_90_CLOCKWISE)
    # from siteplan_qualitycontrol.basic import image_view
    # image_view(sub_img)
    # for information part, the font is too thin, erode is used to make it bold
    kernel = np.ones((2, 2), np.uint8)
    sub_img = cv2.erode(sub_img, kernel)

    df = text_extract(sub_img, custom_config=r'--oem 3 --psm 6')
    # do some correction on the ocr text results
    df = ocr_text_correction(sub_img, df)
    block_df = block_extract(df)

    for i in range(1, len(block_df)):
        if np.abs(block_df["height"].iloc[i-1] - block_df["height"].iloc[i]) >= 5:
            break
    title = " ".join(block_df["text"].iloc[:i])
    address = " ".join(block_df["text"].iloc[i:])

    # for i in range(1, len(df)):
    #     if np.abs(df["height"].iloc[i-1] - df["height"].iloc[i]) >= 10:
    #         break
    # title = " ".join(df["text"].iloc[:i])
    # address = " ".join(df["text"].iloc[i:])

    # save the contour information to locate the info
    save_contours = {"title & address": sub_img_contours.tolist()}
    # generate information
    information = {"title": title, 
                   "address": address, 
                   "contours": save_contours}
    
    return information
