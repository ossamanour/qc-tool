"""
Functions of tools for arrow tip template.
"""
import os
import json
import cv2

from siteplan_qualitycontrol.utils import global_var


def arrow_tip_template_call():
    """
    Call the arrow tip template.

    @return: img_path: path to the arrow tip template.
    """
    img_path = os.path.join(global_var.ROOT, "assets", "arrow_tip.png")
    # image = cv2.imread(img_path)
    return img_path
