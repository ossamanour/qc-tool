"""
Perform zoning module.
"""
import os
from pathlib import Path
import json
import cv2

from siteplan_qualitycontrol.analysis import information_generate
from siteplan_qualitycontrol.basic import address_zoning_info_generate, apn_zoning_info_generate


def zoning_information_generate(
        orig_img_path: str = None):
    """
    Detecte and generate zoning information from siteplan image.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # detect basic information from sidebar
    information_generate(orig_img_path)

    # read in the information
    with open(os.path.join(data_save_path, "information.json"), "r") as fp:
        information = json.load(fp)

    zoning_info = {}
    # detect zoning from address
    address = information["address"]
    zoning_info["address"] = address_zoning_info_generate(address)

    # detect zoning from apn
    apn_list = information["apn_list"]
    for apn in apn_list:
        zoning_info[apn] = apn_zoning_info_generate(apn)

    # go through all the detected zone and get one final result
    zoning_info["summary"] = {"status": "fail", 
                              "error message": "no zoning info found"}
    for key in zoning_info.keys():
        info = zoning_info[key]
        if info["status"] == "succeed":
            zoning_info["summary"] = info
            break
      
    # save the results
    with open(os.path.join(data_save_path, "zone.json"), "w") as fp:
        json.dump(zoning_info, fp, indent=4)


def zoning_post(
        orig_img_path: str = None):
    """
    Return the information of zoning.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # read in the image
    original_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load zoning information
    with open(os.path.join(data_save_path, "zone.json"), "r") as fp:
        zoning_info = json.load(fp)

    return_info = zoning_info["summary"]
    return return_info
