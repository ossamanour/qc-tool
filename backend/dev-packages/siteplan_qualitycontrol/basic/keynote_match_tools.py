"""
Functions of tools for keynote match task.
"""
import os
from pathlib import Path
import json
import cv2
import pandas as pd
from pandas import DataFrame
import numpy as np

from siteplan_qualitycontrol.utils import match_template, contours_generate, contour_outer_maskout
from siteplan_qualitycontrol.basic import keynote_draw
from siteplan_qualitycontrol.images import image_num_let_read


def keynote_match_prepare(
        orig_img_path: str = None):
    """
    Prepare the siteplan image for keynote matching task.
    Including creating folder to save the detected keynotes.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    """
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    image = cv2.imread(orig_img_path)

    # mask out all detected keynotes, prepare for the matching
    with open(os.path.join(data_save_path, "keynote.json"), "r") as fp:
        information = json.load(fp)
    keynote_clean_image = keynote_draw(information, image, (255, 255, 255), -1)
    cv2.imwrite(os.path.join(img_save_path, "keynote_clean.png"), keynote_clean_image)

    # create folders to put the match results
    keynote_data_save_path = os.path.join(data_save_path, "keynote_match")
    os.makedirs(keynote_data_save_path, exist_ok=True)
    keynote_img_save_path = os.path.join(img_save_path, "keynote_match")
    os.makedirs(keynote_img_save_path, exist_ok=True)


def single_keynote_match_draw(
        match_df: DataFrame = None, 
        image: np.array = None, 
        original_info: tuple = None, 
        color: tuple = (255, 0, 0), 
        thickness: int = 2):
    """
    Draw the mathces of one keynote.

    @param: match_df: dataframe containing all matches for one keynote.
    @param: image: array of image to draw.
    @param: original_info: loation information for the original keynotes (in the keynote list).
    @param: color: tuple of color.
    @param: thickness: thickness for drawing.

    @return: display_image: image with matches for one keynote boxed out.
    """
    display_image = image.copy()
    for i in range(len(match_df)):
        x, y, w, h, _ = match_df.iloc[i]
        cv2.rectangle(display_image, (int(x), int(y)), (int(x+w), int(y+h)), color, thickness)
        cv2.putText(display_image, f"match {i+1}", (int(x), int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)
    # add original if original is given
    if original_info:
        (kx, ky, kw, kh) = original_info
        cv2.rectangle(display_image, (kx, ky), (kx+kw, ky+kh), color, thickness)
        cv2.putText(display_image, f"original", (kx, ky-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)

    return display_image


def single_keynote_match(
        image: np.array = None, 
        keynote_df: DataFrame = None, 
        index: int = None, 
        keynote_folder: str = None, 
        match_threshold: float = 0.7, 
        display_image: np.array = None, 
        match_status_image: np.array = None):
    """
    Perform keynote matching for one keynote.

    @param: image: array of image to do the matching.
    @param: keynote_df: dataframe containing information of all detected keynotes.
    @param: index: index for the keynote to perform matching.
    @param: keynote_folder: path to the folder where the detected keynote images are saved.
    @param: match_threshold: threshold for matching algorithm, can be customized.
    @param: display_image: array of image to draw the results.
    @param: match_status_image: this is used for the frontend to show the matching one by one.

    @return: new_match_df: dataframe containing all matches. 
    @return: keynote_match_image: image with keynote matches boxed out. 
    @return: single_match_status_image:  
    @return: match_status_image:
    """
    # match one template based on the index 
    (kimg, kx, ky, kw, kh, text, tx, ty, tw, th, tth, kid, kcontour, kmatch, khierarch, keyword) = keynote_df.iloc[index]
    
    keynote_image = cv2.imread(os.path.join(keynote_folder, kimg))
    match_df = match_template(image=image, 
                              template=keynote_image, 
                              match_threshold=match_threshold)

    # clean based on the keyword
    new_match_df = DataFrame()
    for i in range(len(match_df)):
        # read in the match sub image
        x, y, w, h, _ = match_df.iloc[i]
        sub_match_img = image[int(y):int(y+h), int(x):int(x+w), :]
        contours, hierarchy = contours_generate(sub_match_img)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        return_image = contour_outer_maskout(sub_match_img, sorted_contours[1])
        return_image = cv2.drawContours(return_image, [sorted_contours[1]], -1, (255, 255, 255), 2)

        string = image_num_let_read(return_image)

        if string == keyword:
            new_match_df = pd.concat([new_match_df, match_df.iloc[i].to_frame().transpose()], ignore_index=True, sort=False)

    if display_image is None:
        # if no display image given, draw on the match image
        display_image = image.copy()

    # draw the found match 
    original_info = (kx, ky, kw, kh)
    keynote_match_image = single_keynote_match_draw(new_match_df, display_image, original_info)
    
    # update the display image if needed
    # if match_status_image is not None:
    single_match_status_image = single_keynote_match_draw(new_match_df, match_status_image)
    # draw the red/green to indicate match results
    # update the whole match status image
    if len(new_match_df) == 0:
        # mark red if no match found
        cv2.rectangle(single_match_status_image, (kx, ky), (kx+kw, ky+kh), (0, 0, 255), 2)
        cv2.rectangle(match_status_image, (kx, ky), (kx+kw, ky+kh), (0, 0, 255), 2)
    else:
        # mark green is found match
        cv2.rectangle(single_match_status_image, (kx, ky), (kx+kw, ky+kh), (0, 255, 0), 2)
        cv2.rectangle(match_status_image, (kx, ky), (kx+kw, ky+kh), (0, 255, 0), 2)
    # else:
    #     single_match_status_image = None

    return new_match_df, keynote_match_image, single_match_status_image, match_status_image


def keynote_initial_draw(
        orig_img_path: str = None):
    """
    For GUI use only. Initialize the image for GUI display on keynote matching task.

    @param: orig_img_path: path to the original image, PNG format.
    """
    # save path
    # sa_clean_nokl_img_path = os.path.join(Path(orig_img_path).parent, "sa_clean_nokl.png")
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    # keynote info
    keynote_folder = os.path.join(data_save_path, "keynotes")
    keynote_df = pd.read_csv(os.path.join(keynote_folder, "keynote.csv"))

    display_image = cv2.imread(orig_img_path)
    for i in range(len(keynote_df)):
        (kimg, kx, ky, kw, kh, text, tx, ty, tw, th, tth, kid, kcontour, kmatch, khierarch, key) = keynote_df.iloc[i]
        cv2.rectangle(display_image, (kx, ky), (kx+kw, ky+kh), (150, 150, 150), 3)

    cv2.imwrite(os.path.join(img_save_path, "keynote_match_results.png"), display_image)

# # for GUI and web application use, to show match results for each keynote
# def keynote_display_draw(
#         orig_img_path: str = None, 
#         keynote_df: DataFrame = None, 
#         index: int = None):
    
    


