"""
Functions to generate keynote templates.
"""
import os
import cv2
import numpy as np
import json

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate


def keynote_template_clean(
        template: np.array = None):
    """
    Clean the generated keynote template, mask out the number inside.

    @param: template: numpy array containing the initial keynote template.

    @return: template_return: cleaned template image.
    """
    template_return = template.copy()
    contours, _ = contours_generate(template)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cv2.drawContours(template_return, [sorted_contours[1]], -1, (255, 255, 255), -1)
    return template_return


def keynote_template_generate():
    """
    Generate the templates for keynote notation. 
    Now support two: irregular pentagon, regular rhombus
    """
    source_dir = os.path.join(global_var.ROOT, "template_source_images", "keynotes")
    save_dir = os.path.join(global_var.ROOT, "assets", "keynotes")

    # generate config file 
    config = {}

    # generate shape <irregular pentagon>
    source_image = cv2.imread(os.path.join(source_dir, "irregular_pentagon_src.png"))
    keynote = source_image[2175:2270, 8275:8370, :]
    keynote_clean = keynote_template_clean(keynote)
    # save the template
    cv2.imwrite(os.path.join(save_dir, "irregular_pentagon.png"), keynote_clean)

    # config
    contours, _ = contours_generate(keynote_clean, 
                                    thresh=127, 
                                    type=cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU, 
                                    mode=cv2.RETR_CCOMP, 
                                    method=cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    config["irregular_pentagon"] = {"path": os.path.join("assets", "keynotes", "irregular_pentagon.png"), 
                                    "contours": sorted_contours[1].tolist()}

    # generate shape <regular rhombus>
    source_image = cv2.imread(os.path.join(source_dir, "regular_rhombus_src.png"))
    keynote = source_image[805:930, 8045:8170, :]
    keynote_clean = keynote_template_clean(keynote)
    # save the template
    cv2.imwrite(os.path.join(save_dir, "regular_rhombus.png"), keynote_clean)
    
    # config
    contours, _ = contours_generate(keynote_clean, 
                                    thresh=127, 
                                    type=cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU, 
                                    mode=cv2.RETR_CCOMP, 
                                    method=cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    config["regular_rhombus"] = {"path": os.path.join("assets", "keynotes", "regular_rhombus.png"), 
                                 "contours": sorted_contours[1].tolist()}
    
    config_save_path = os.path.join(save_dir, "config.json")
    with open(config_save_path, "w") as fp:
        json.dump(config, fp, indent=4)

