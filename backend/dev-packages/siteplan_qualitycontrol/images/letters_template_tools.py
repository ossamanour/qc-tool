"""
Functions of tools for letter templates.
"""
import os
import json
import numpy as np
import cv2

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate


def letter_template_call(
        l: str = None):
    """
    Call the templates of input letter.

    @param: l: input letter.

    @return: img_path: path to the letter template image.
    @return: img_contours: contours for the letter template.
    """
    # read in config file
    config_file = os.path.join(global_var.ROOT, "assets", "letters", "config.json")
    with open(config_file, "r") as f:
        config = json.load(f)
    img_path = os.path.join(global_var.ROOT, config[l.upper()]["path"])
    img_contours = np.array(config[l.upper()]["contours"])
    return img_path, img_contours


def letter_template_match(
        input_contour: np.array = None):
    """
    Perform matching over all letters.

    @param: input_contour: array of contour that need to be matched.

    @return: l: the letter of that matches the input contour most. 
    """
    # read in config file
    config_file = os.path.join(global_var.ROOT, "assets", "letters", "config.json")
    with open(config_file, "r") as f:
        config = json.load(f)

    # do matching
    sd = cv2.createShapeContextDistanceExtractor()
    scores = {}
    for key in config.keys():
        letter_contours = np.array(config[key]["contours"])
        scores[key] = sd.computeDistance(letter_contours, input_contour)
    # get the best match
    l = min(scores, key=scores.get)

    return l


def image_letter_read(
        image: np.array = None):
    """
    Read the letter from an input image.

    @param: image: array of input image.

    @return: letter: detected letter.
    """
    target = image.copy()
    # find contours, same contour generation rule with the letter template
    contours, _ = contours_generate(target, 
                                    mode=cv2.RETR_EXTERNAL, 
                                    method=cv2.CHAIN_APPROX_NONE)
    # sort contours by location, left to right
    sorted_contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    letter = ""
    for c in sorted_contours:
        l = letter_template_match(c)
        letter = letter + l

    return letter