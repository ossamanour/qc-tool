"""
Functions to generate HPD landscape template, including configure information.
"""
import os
import cv2
import json

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate


def hpd_landscape_template_generate():
    """
    Generate HPD landscape template, including configure information.
    Only used once by the developer.
    """
    # create save folder
    os.makedirs(os.path.join(global_var.ROOT, "assets", "companies", "hpd"), exist_ok=True)

    ls_src = cv2.imread(os.path.join(global_var.ROOT, "template_source_images", "company_templates", "hpd_landscape.png"))

    # cover the main portion of landscape
    return_image = ls_src.copy()
    return_image[81:7114, 303:9153, :] = 255
    return_image[81:6687, 9150:9848, :] = 255

    # the content of the sidebar info portion of landscape
    return_image[2413:3393, 9983:10528, :] = 255
    return_image[5105:5155, 9958:10345, :] = 255
    return_image[5102:5150, 10389:10544, :] = 255
    return_image[5493:5550, 9984:10497, :] = 255
    return_image[5570:5620, 10219:10332, :] = 255
    return_image[5646:5691, 10217:10327, :] = 255
    return_image[5711:5760, 10219:10406, :] = 255
    return_image[5785:5830, 10220:10320, :] = 255
    return_image[6132:6225, 10570:10608, :] = 255
    return_image[6480:7022, 9920:10530, :] = 255

    save_path = os.path.join(global_var.ROOT, "assets", "companies", "hpd", "landscape_template.png")
    cv2.imwrite(save_path, return_image)

    # generate config file
    contours, _ = contours_generate(return_image)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    config = {}
    config["original"] = [0, 0, return_image.shape[1], return_image.shape[0]]
    config["main"] = cv2.boundingRect(sorted_contours[1])
    config["sidebar"] = cv2.boundingRect(sorted_contours[2])
    config["copyright_P"] = cv2.boundingRect(sorted_contours[6])
    config["hpd_logo"] = cv2.boundingRect(sorted_contours[4])
    config["project_address_P"] = cv2.boundingRect(sorted_contours[5])
    config["plan_info"] = cv2.boundingRect(sorted_contours[3])
    config["scale_ruler"] = cv2.boundingRect(sorted_contours[9])
    config["page_info"] = cv2.boundingRect(sorted_contours[10])
    config["az_bluestake"] = cv2.boundingRect(sorted_contours[13])

    config_save_path = os.path.join(global_var.ROOT, "assets", "companies", "hpd", "landscape_config.json")
    with open(config_save_path, "w") as fp:
        json.dump(config, fp, indent=4)