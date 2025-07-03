"""
Functions to generate SEG siteplan template, including configure information.
"""
import os
import cv2
import json

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate


def seg_siteplan_template_generate():
    """
    Generate SEG siteplan template, including configure information.
    Only used once by the developer.
    """
    # create save folder
    os.makedirs(os.path.join(global_var.ROOT, "assets", "companies", "seg"), exist_ok=True)

    sp_src = cv2.imread(os.path.join(global_var.ROOT, "template_source_images", "company_templates", "seg_siteplan.png"))

    contours, _ = contours_generate(sp_src)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # the content of the main portion of siteplan
    (x, y, w, h) = cv2.boundingRect(sorted_contours[1])
    return_image = sp_src.copy()
    return_image[y:y+h, x:x+w, :] = 255

    # find contours on the cleaned image
    contours, _ = contours_generate(return_image)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # the content of the sidebar info portion of siteplan
    (x, y, w, h) = cv2.boundingRect(sorted_contours[4])
    return_image[y:y+h, x:x+w, :] = 255
    (x, y, w, h) = cv2.boundingRect(sorted_contours[5])
    return_image[y:y+h, x:x+w, :] = 255

    # cover all the other information protal
    return_image[6890:7000, 9849:10077, :] = 255
    return_image[6890:7000, 10196:10417, :] = 255
    return_image[6544:6700, 9913:10309, :] = 255
    return_image[6306:6396, 9980:10276, :] = 255
    return_image[5734:5813, 9945:10327, :] = 255
    return_image[5590:5658, 9989:10244, :] = 255
    return_image[5259:5537, 10124:10458, :] = 255
    return_image[4856:5243, 9855:9972, :] = 255
    return_image[4739:5240, 10213:10409, :] = 255

    save_path = os.path.join(global_var.ROOT, "assets", "companies", "seg", "siteplan_template.png")
    cv2.imwrite(save_path, return_image)

    # generate config file
    contours, _ = contours_generate(return_image)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    config = {}
    config["original"] = [0, 0, return_image.shape[1], return_image.shape[0]]
    config["main"] = cv2.boundingRect(sorted_contours[1])
    config["sidebar"] = cv2.boundingRect(sorted_contours[2])
    config["top_info"] = cv2.boundingRect(sorted_contours[5])
    config["seg_logo_P"] = cv2.boundingRect(sorted_contours[3])
    config["customer_logo_P"] = cv2.boundingRect(sorted_contours[4])
    config["az811"] = cv2.boundingRect(sorted_contours[9])
    config["project_P"] = cv2.boundingRect(sorted_contours[8])
    config["location_P"] = cv2.boundingRect(sorted_contours[7])
    config["staff_info"] = cv2.boundingRect(sorted_contours[11])
    config["issued_for"] = cv2.boundingRect(sorted_contours[10])
    config["revision_no"] = cv2.boundingRect(sorted_contours[20])
    config["job_no"] = cv2.boundingRect(sorted_contours[17])
    config["sheet_title"] = cv2.boundingRect(sorted_contours[6])
    config["page_no"] = cv2.boundingRect(sorted_contours[19])
    config["sheet_no"] = cv2.boundingRect(sorted_contours[18])

    config_save_path = os.path.join(global_var.ROOT, "assets", "companies", "seg", "siteplan_config.json")
    with open(config_save_path, "w") as fp:
        json.dump(config, fp, indent=4)