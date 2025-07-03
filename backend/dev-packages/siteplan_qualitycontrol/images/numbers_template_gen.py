"""
Functions to generate all templates for number 0-9.
"""

import os
import cv2
import json

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate


def numbers_generate():
    """
    Generate templates for number 0-9.
    This only used once by the developer.
    """
    source_dir = os.path.join(global_var.ROOT, "template_source_images", "numbers")
    save_dir = os.path.join(global_var.ROOT, "assets", "numbers")
    # get the source image and mask out where not needed
    source_image = cv2.imread(os.path.join(source_dir, "original.png"))

    # 0
    img_0 = cv2.imread(os.path.join(source_dir, "img_1.png"))
    img_0[:, 0:36, :] = 255
    # img_0 = cv2.resize(img_0, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num0.png"), img_0)

    # 1
    img_1 = cv2.imread(os.path.join(source_dir, "img_3.png"))
    img_1[:, 29:, :] = 255
    # img_1 = cv2.resize(img_1, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num1.png"), img_1)

    # 2
    img_2 = cv2.imread(os.path.join(source_dir, "img_1.png"))
    img_2[:, 37:, :] = 255
    # img_2 = cv2.resize(img_2, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num2.png"), img_2)

    # 3
    img_3 = cv2.imread(os.path.join(source_dir, "img_4.png"))
    img_3[:, 37:, :] = 255
    # img_3 = cv2.resize(img_3, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num3.png"), img_3)

    # 4
    img_4 = cv2.imread(os.path.join(source_dir, "img_3.png"))
    img_4[:, 0:29, :] = 255
    # img_4 = cv2.resize(img_4, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num4.png"), img_4)

    # 5
    img_5 = cv2.imread(os.path.join(source_dir, "img_0.png"))
    # img_5 = cv2.resize(img_5, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num5.png"), img_5)

    # 6
    img_6 = source_image[3786:3838, 1950:2006, :]
    img_6[:, 28:, :] = 255
    # img_6 = cv2.resize(img_6, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num6.png"), img_6)

    # 7
    img_7 = source_image[5080:5127, 4503:4559, :]
    img_7[:, 28:, :] = 255
    # img_7 = cv2.resize(img_7, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num7.png"), img_7)

    # 8
    img_8 = cv2.imread(os.path.join(source_dir, "img_11.png"))
    # img_8 = cv2.resize(img_8, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num8.png"), img_8)

    # 9
    img_9 = cv2.imread(os.path.join(source_dir, "img_9.png"))
    # img_9 = cv2.resize(img_9, (100, 100))
    cv2.imwrite(os.path.join(save_dir, "num9.png"), img_9)

    # generate config file
    config = {}

    for i in range(10):
        num_img_path = os.path.join(global_var.ROOT, "assets", "numbers", f"num{i}.png")
        num_image = cv2.imread(num_img_path)
        contours, _ = contours_generate(num_image, 
                                        thresh=127, 
                                        mode=cv2.RETR_EXTERNAL, 
                                        method=cv2.CHAIN_APPROX_NONE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        config[i] = {"path": os.path.join("assets", "numbers", f"num{i}.png"),
                     "contours": sorted_contours[0].tolist()}
    
    config_save_path = os.path.join(global_var.ROOT, "assets", "numbers", "config.json")
    with open(config_save_path, "w") as fp:
        json.dump(config, fp, indent=4)




    


