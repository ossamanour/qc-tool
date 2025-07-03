"""
Functions for tools of number templates.
"""
import os
import json
import numpy as np
import cv2

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate


def number_template_call(
        i: int = None):
    """
    Call templates by number.

    @param: number: integer for unber, from 0 to 9.

    @return: img_path: path to the number template image.
    @return: img_contours: contours for the number template.
    """
    # read in config file
    config_path = os.path.join(global_var.ROOT, "assets", "numbers", "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    img_path = os.path.join(global_var.ROOT, config[i]["path"])
    img_contours = np.array(config[i]["contours"])
    return img_path, img_contours


def number_template_match(
        input_contour: np.array = None):
    """
    Perform matching over all numbers.

    @param: input_contour: array of contour that need to be matched.

    @return: n: the number of that matches the input contour most. 
    """
    # read in config file
    config_path = os.path.join(global_var.ROOT, "assets", "numbers", "config.json")
    with open(config_path, "r") as fp:
        config = json.load(fp)

    # do matching
    sd = cv2.createShapeContextDistanceExtractor()
    scores = {}
    for key in config.keys():
        num_contours = np.array(config[key]["contours"])
        scores[key] = sd.computeDistance(num_contours, input_contour)
    # get the best match
    n = min(scores, key=scores.get)

    return n


def image_number_read(
        image: np.array = None):
    """
    Read the number from an input image.

    @param: image: array of input image.

    @return: number: detected number.
    """
    target = image.copy()
    # find contours, same contour generation rule with the number template
    contours, _ = contours_generate(target, 
                                    mode=cv2.RETR_EXTERNAL, 
                                    method=cv2.CHAIN_APPROX_NONE)
    # sort contours by location, left to right
    sorted_contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    number = ""
    for c in sorted_contours:
        n = number_template_match(c)
        number = number + n

    return number