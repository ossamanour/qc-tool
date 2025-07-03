"""
Functions of tools for both numbers and letters.
"""
import os
import json
import numpy as np
import cv2

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate


def num_let_template_match(
        input_contour: np.array = None):
    """
    Perform matching on number and letter templates

    @param: input_contour: detected contour on which the matching will be performed.

    @return: n: best match number/letter.
    """
    # read in number config file
    config_path = os.path.join(global_var.ROOT, "assets", "numbers", "config.json")
    with open(config_path, "r") as fp:
        num_config = json.load(fp)
    # read in letter config file
    config_file = os.path.join(global_var.ROOT, "assets", "letters", "config.json")
    with open(config_file, "r") as fp:
        let_config = json.load(fp)
    # merge together
    config = num_config | let_config

    # do matching
    sd = cv2.createShapeContextDistanceExtractor()
    scores = {}
    for key in config.keys():
        num_contours = np.array(config[key]["contours"])
        scores[key] = sd.computeDistance(num_contours, input_contour)
    # get the best match
    n = min(scores, key=scores.get)

    return n


def image_num_let_read(
        image: np.array = None):
    """
    Read the number and letter on given image.

    @param: image: array of input image.

    @return: string: detected string, consisting of number and/or letter.
    """
    target = image.copy()
    # find contours, same contour generation rule wiht the template
    contours, _ = contours_generate(target, 
                                    mode=cv2.RETR_EXTERNAL, 
                                    method=cv2.CHAIN_APPROX_NONE)
    # sort contours by location, left to right
    sorted_contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    string = ""
    for c in sorted_contours:
        l = num_let_template_match(c)
        string = string + l

    return string