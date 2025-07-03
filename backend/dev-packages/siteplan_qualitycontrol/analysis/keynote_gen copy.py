import os
from pathlib import Path
import cv2
import json
import pandas as pd

from siteplan_qualitycontrol.images import keynote_template_call
from siteplan_qualitycontrol.basic import keynote_list_title_find, match_keynote_notation, match_keynote_clean, keynote_pair_generate, keynote_draw
from siteplan_qualitycontrol.utils import draw_contours_from_df, dataframe_save


def keynote_generate(
        orig_img_path: str = None, 
        keynote_template_name: str = None):
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    # use the original image as display image
    display_image = cv2.imread(orig_img_path)

    # read in the image, image used here is the body image
    body_image = cv2.imread(os.path.join(img_save_path, "body.png"))
    
    # read in the keynote template
    template_img_path, template_contour = keynote_template_call(keynote_template_name)

    # find match of keynote template
    keynote_match_df = match_keynote_notation(body_image, template_contour)
    keynote_match_image = draw_contours_from_df(keynote_match_df, display_image)
    dataframe_save(keynote_match_df, os.path.join(data_save_path, "keynote_match.csv"))
    cv2.imwrite(os.path.join(img_save_path, "keynote_match.png"), keynote_match_image)

    # find keynote list title
    block_df = pd.read_csv(os.path.join(data_save_path, "paragraph.csv"))
    keynote_title_df = keynote_list_title_find(block_df)
    # no keynote list detected case
    # TODO: for keynote list title not in the saved global var
    if len(keynote_title_df) == 0:
        keynote_generate_info = {"status": "fail", 
                                 "error message": "no keynote list title detected"}
        # save the results
        with open(os.path.join(data_save_path, "keynote.json"), "w") as fp:
            json.dump(keynote_generate_info, fp, indent=4)
        return None

    # clean up the matches with keynote template
    keynote_match_clean_df = match_keynote_clean(keynote_match_df, template_contour, keynote_title_df)
    # no keynote match after clean up
    if len(keynote_match_clean_df) == 0:
        keynote_generate_info = {"status": "fail", 
                                 "error message": "no keynote template match detected"}
        # save the results
        with open(os.path.join(data_save_path, "keynote.json"), "w") as fp:
            json.dump(keynote_generate_info, fp, indent=4)
        return None
    
    keynote_match_clean_image = draw_contours_from_df(keynote_match_clean_df, display_image)
    dataframe_save(keynote_match_clean_df, os.path.join(data_save_path, "keynote_match_clean.csv"))
    cv2.imwrite(os.path.join(img_save_path, "keynote_match_clean.png"), keynote_match_clean_image)
    
    # generate keynote text pair and save
    key_folder = os.path.join(data_save_path, "keynotes")
    os.makedirs(key_folder, exist_ok=True)
    keynote_pair_df = keynote_pair_generate(orig_img_path, key_folder, keynote_match_clean_df, block_df)

    # create keynote generate return information
    keynote_generate_info = {"status": "succeed"}
    keynote_generate_info.update(json.loads(keynote_title_df.iloc[0].to_json()))
    keynote_generate_info["key_folder"] = key_folder
    keynote_generate_info["total_keynotes"] = len(keynote_pair_df)

    # draw the keynote results
    keynote_pair_image = keynote_draw(keynote_generate_info, display_image)
    cv2.imwrite(os.path.join(img_save_path, "keynote_pair.png"), keynote_pair_image)

    # save the results
    with open(os.path.join(data_save_path, "keynote.json"), "w") as fp:
        json.dump(keynote_generate_info, fp, indent=4)


def keynote_generate_post(
        orig_img_path: str = None, 
        index: int = None):
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")

    # load keynote generation information
    with open(os.path.join(data_save_path, "keynote.json"), "r") as fp:
        keynote_generate_info = json.load(fp)

    if index is None:
        return keynote_generate_info
    else:
        return keynote_generate_info[f"keynote-{index+1}"]