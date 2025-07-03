"""
Functions to generate all templates for letters.
"""
import os
import cv2
import json

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate
from siteplan_qualitycontrol.utils import image_view


def letters_generate():
    """
    Generate templates for letters.
    This only used once by the developer.
    """
    source_dir = os.path.join(global_var.ROOT, "template_source_images", "letters")
    save_dir = os.path.join(global_var.ROOT, "assets", "letters")

    # A
    img_A = cv2.imread(os.path.join(source_dir, "img_1.png"))
    img_A[:, 0:42, :] = 255
    img_A[0:64, 0:47, :] = 255
    cv2.imwrite(os.path.join(save_dir, "letterA.png"), img_A)

    # B
    img_B = cv2.imread(os.path.join(source_dir, "img_2.png"))
    img_B[:, 0:47, :] = 255
    cv2.imwrite(os.path.join(save_dir, "letterB.png"), img_B)

    # C
    img_C = cv2.imread(os.path.join(source_dir, "img_3.png"))
    img_C[:, 0:35, :] = 255
    cv2.imwrite(os.path.join(save_dir, "letterC.png"), img_C)

    # generate config file
    config = {}
    
    letter_list = ["A", "B", "C"]
    for l in letter_list:
        letter_img_path = os.path.join(save_dir, f"letter{l}.png")
        letter_image = cv2.imread(letter_img_path)
        contours, _ = contours_generate(letter_image, 
                                        thresh=127, 
                                        mode=cv2.RETR_EXTERNAL, 
                                        method=cv2.CHAIN_APPROX_NONE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        config[l] = {"path": os.path.join("assets", "letters", f"letter{l}.png"), 
                     "contours": sorted_contours[0].tolist()}
        
    config_save_path = os.path.join(save_dir, "config.json")
    with open(config_save_path, "w") as fp:
        json.dump(config, fp, indent=4)
