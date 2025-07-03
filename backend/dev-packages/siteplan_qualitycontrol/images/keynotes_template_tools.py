"""
Function of tools for keynote templates.
"""
import os
import json
import cv2
import numpy as np

from siteplan_qualitycontrol.utils import global_var


def keynote_template_call(
        name: str = None):
    """
    Call keynote templated by name.

    @param: name: name of keynote template.

    @return: img_path: path to the number template image.
    @return: img_contours: contours for the number template.
    """
    # read in config file
    config_path = os.path.join(global_var.ROOT, "assets", "keynotes", "config.json")
    with open(config_path, "r") as fp:
        config = json.load(fp)
    img_path = os.path.join(global_var.ROOT, config[name]["path"])
    img_contours = np.array(config[name]["contours"])
    return img_path, img_contours


def list_keynote_template():
    """
    List all available keynote templates.

    @return: keynote_template_list: list of names for all available keynote templates.
    """
    # read in config file
    config_path = os.path.join(global_var.ROOT, "assets", "keynotes", "config.json")
    with open(config_path, "r") as fp:
        config = json.load(fp)
    keynote_template_list = config.keys()

    return keynote_template_list
