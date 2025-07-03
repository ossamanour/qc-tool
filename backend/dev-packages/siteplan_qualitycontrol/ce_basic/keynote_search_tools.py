"""
Functions of tools for keynote search.
"""
import pandas as pd
import re
import numpy as np
from pandas import DataFrame
import cv2


def get_keynote_with_words(
        keynote_df: DataFrame = None, 
        word_list: list = None):
    """
    From already detected keynote list, get keynote by keywords.

    @param: keynote_df: dataframe containing all detected keynotes.
    @param: word_list: list of possible keywords to search.

    @return: detected_df: dataframe of keynotes that contain keywords.
    """
    detected_df = DataFrame()
    for i in range(len(keynote_df)):
        text = keynote_df.iloc[i].text
        # clean up, remove some '.', keep only letters and spaces
        clean_text = re.sub(r'[^a-zA-Z\s]', '', text)
        if all(word in clean_text for word in word_list):
            # set ignore_index to False to keep the index, for later keynote matching
            detected_df = pd.concat([detected_df, DataFrame([keynote_df.iloc[i]])], ignore_index=False, sort=False)

    return detected_df


def get_keynote_with_words_sets(
        keynote_df: DataFrame = None, 
        word_list_set: list = None):
    """
    From already detected keynote list, get keynote by keywords, a set of keywords will be tried.

    @param: keynote_df: dataframe containing all detected keynotes.
    @param: word_list_set: set of lists of possible keywords to search.

    @return: return_info: dictionary containing detection results, containing detected_df if any keynote is found.
    """
    for word_list in word_list_set:
        detected_df = get_keynote_with_words(keynote_df, word_list)
        if len(detected_df) != 0:
            break

    if len(detected_df) == 0:
        return_info = {"status": "fail"}
    else:
        return_info = {"status": "succeed", 
                       "detected_df": detected_df}
    
    return return_info


def keynote_match_draw(
        detected_df: DataFrame = None, 
        match_df: DataFrame = None, 
        image: np.array = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 3):
    """
    Draw matches of keynote on the input image.

    @param: detected_df: dataframe of information for the keynote to be used for matching.
    @param: match_df: dtaframe containing all matches that found.
    @param: image: array of image to be drawn on.
    @param: color: tuple of color.
    @param: thickness: thickness for drawing.

    @return: display_image: image with the original keynote and its matches boxed out.
    """
    display_image = image.copy()
    # box out the keynote 
    (kimg, kx, ky, kw, kh, text, tx, ty, tw, th, tth, kid, kcontour, kmatch, khierarch, key) = detected_df.iloc[0]
    cv2.rectangle(display_image, (kx, ky), (kx+kw, ky+kh), (255, 0, 255), 3)
    for i in range(len(match_df)):
        x, y, w, h, score = match_df.iloc[i]
        cv2.rectangle(display_image, (int(x), int(y)), (int(x+w), int(y+h)), color, thickness)
        cv2.putText(display_image, text, (int(x-10), int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness)

    return display_image