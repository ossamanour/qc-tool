"""
Perform scale module.
"""
import os
from pathlib import Path
import json
import cv2
import json

from siteplan_qualitycontrol.company_config import COMPANY_FUNC_LISTS


def scale_generate(
        orig_img_path: str = None):
    """
    Detect scale ruler from siteplan.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    # use original image as display image
    display_image = cv2.imread(orig_img_path)

    # read the config file to choose which compnay template is used
    with open(os.path.join(Path(orig_img_path).parents[1], "config.json"), "r") as fp:
        config = json.load(fp)
        company = config["company"]

    # generate scale
    scale_info_generate = COMPANY_FUNC_LISTS.get(company).get("scale_generate")
    scale_info = scale_info_generate(orig_img_path)

    # box out the scale ruler bar and save the image
    x, y, w, h = scale_info["scale_loc"]
    cv2.rectangle(display_image, (x, y), (x+w, y+h), (255, 0, 255), 1)
    scale_number = scale_info["scale_number"]
    cv2.putText(display_image, str(scale_number), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 1)
    cv2.imwrite(os.path.join(img_save_path, "scale_ruler.png"), display_image)

    # save the scale information
    with open(os.path.join(data_save_path, "scale.json"), "w") as fp:
        json.dump(scale_info, fp, indent=4)


def scale_post(
        orig_img_path: str = None):
    """
    Return scale information of siteplan.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load the scale information
    with open(os.path.join(data_save_path, "scale.json"), "r") as fp:
        scale_info = json.load(fp)

    return scale_info    
