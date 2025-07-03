"""
Functions to generate arrow tip template.
"""
import os
import json
import cv2
import numpy as np

from siteplan_qualitycontrol.utils import global_var


def arrow_tip_template_generate():
    """
    Functions to generate arrow tip template.
    This only used once by the developer.
    """
    source_img_path = os.path.join(global_var.ROOT, "template_source_images", "seg_templates", "source.png")
    source_image = cv2.imread(source_img_path)
    # get the template for the arrow tip
    arrow = source_image[1200:1250, 3580:3600, :]
    #clean up
    arrow[0:25, 19, :] = 255
    arrow[0:24, 18, :] = 255
    arrow[0:22, 17, :] = 255
    arrow[0:20, 16, :] = 255
    arrow[0:18, 15, :] = 255
    arrow[0:16, 14, :] = 255
    arrow[0:14, 13, :] = 255
    arrow[-1, :, :] = 255

    # save the template
    cv2.imwrite(os.path.join(global_var.ROOT, "assets", "arrow_tip.png"), arrow)