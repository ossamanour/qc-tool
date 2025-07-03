"""
Functions of tools for keynote related.
"""
import os
from pathlib import Path
import pandas as pd
import cv2
from pandas import DataFrame
import numpy as np

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate, dataframe_save
from siteplan_qualitycontrol.images import keynote_template_call
from siteplan_qualitycontrol.utils import contour_outer_maskout
from siteplan_qualitycontrol.images import image_num_let_read


def keynote_list_title_find(
        block_df: DataFrame = None):
    """
    Go through keynote list titles in the global variable and find the location of keynote list title in the siteplan.
    If not exist, ask the user to input a new one.

    @param: block_df: data frame containing all text blocks (paragraph).

    @return: (key_x, key_y, key_w, key_h, key, key_th): location and text content of the legend list title
    """
    keynote_title_df = DataFrame()
    # for keynote_title in global_var.KEYNOTE_LIST_TITLE:
    for key_id in global_var.KEYNOTE_LIST_TITLE.keys():
        keynote_title = global_var.KEYNOTE_LIST_TITLE[key_id]
        keynote_list = keynote_title.split(" ")
        for i in range(len(block_df)):
            if len([text for text in keynote_list if text in str(block_df.loc[i, 'text'])]) == len(keynote_list):
                keynote_title_df = DataFrame([block_df.iloc[i]])
                return keynote_title_df

    # TODO: let the user to manually input keynote list title
    
    # if no keynote list exist, return empty
    return keynote_title_df


def match_keynote_notation(
        image: np.array = None, 
        template_contour: np.array = None):
    """
    Search for matches on the siteplan for the keynote template.

    @param: image: array of siteplan image.
    @param: template_contour: array of contour for the keynote template.

    @return: match_df: dataframe containing information of all detected matches.
    """
    # do matches on contours
    contours, hierarchys = contours_generate(image, 
                                             thresh=250, 
                                             type=cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU, 
                                             mode=cv2.RETR_CCOMP, 
                                             method=cv2.CHAIN_APPROX_SIMPLE)
    match_df = DataFrame()
    for i, c in enumerate(contours):
        match = cv2.matchShapes(template_contour, c, 1, 0.0)
        if match < 0.05:
            temp = {"id": i, "contour": c, "match": match, "hierarchy": hierarchys[0][i, :]}
            match_df = pd.concat([match_df, DataFrame([temp])], ignore_index=True, sort=False)
    
    return match_df
    

def match_keynote_clean(
        match_df: DataFrame = None, 
        template_contour: np.array = None, 
        keynote_title_df: DataFrame = None):
    """
    Based on location and contour area, clean the detected keynote matches.

    @param: match_df: dataframe containing information of all detected contours with the keynote template.
    @param: template_contour: array of contour for keynote template.
    @param: keynote_title_df: dataframe containing information of the keynote list title.

    @return: match_df_clean: dataframe of the cleaned matches with the keynote template.
    """
    # clean based on location and contour area
    # copy the input data frame to avoid changing the original input
    match_df_clean = match_df.copy()

    # read the location information of keynote list title
    (key_x, key_y, key_w, key_h, key, key_th) = keynote_title_df.iloc[0]

    # clean based on contour area
    template_contour_area = cv2.contourArea(template_contour)
    for i in range(len(match_df_clean)):
        contour = match_df_clean.iloc[i].contour
        contour_area = cv2.contourArea(contour)
        (x, y, w, h) = cv2.boundingRect(contour)
        # check contour area
        if (0.5 * template_contour_area) > contour_area or contour_area > (1.5 * template_contour_area):
            match_df_clean.iloc[i] = None
        # notation of keynotes should not be too left from the keynotes list title 
        # but can be a new column at right side of the title if there are too many
        if (key_x - x) > (2 * w):
            match_df_clean.iloc[i] = None
        # notation of keynotes should not be far above the keynote list title
        if (y + h) < key_y:
            match_df_clean.iloc[i] = None
    match_df_clean.dropna(inplace=True)
    match_df_clean.reset_index(drop=True, inplace=True)

    # clean based on parent relationship, remove duplicated ones of inner and outer deges
    for i in range(len(match_df_clean)):
        parent = match_df_clean.iloc[i].hierarchy[-1]
        if parent != -1:
            # find if parent is one of the matches
            if match_df_clean.id.isin([parent]).any():
                # delete children
                match_df_clean.iloc[i] = None
    match_df_clean.dropna(inplace=True)
    match_df_clean.reset_index(drop=True, inplace=True)

    # clean based on the number of corners
    peri = cv2.arcLength(template_contour, True)
    template_approx = cv2.approxPolyDP(template_contour, 0.04 * peri, True)
    for i in range(len(match_df_clean)):
        contour = match_df_clean.iloc[i].contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        if len(approx) != len(template_approx):
            match_df_clean.iloc[i] = None
    match_df_clean = match_df_clean.dropna()
    match_df_clean = match_df_clean.reset_index(drop=True)

    return match_df_clean


def keynote_key_read(
        key_folder:str = None, 
        match_df: DataFrame = None):
    """
    For all detected keynote template matches, detect and read the correponding key, number(with letter) for the keynote.

    @param: key_folder: path to the folder where all detected keynotes (csv and images) are saved.
    @param: match_df: dataframe containing information of all detected keynotes.

    @return: new_match_df: dataframe of inforamtion for all detected keynotes with read key.
    """
    key_list = []
    for i in range(len(match_df)):
        row = match_df.iloc[i]
        keynote_image = cv2.imread(os.path.join(key_folder, match_df.iloc[i].key_img))
        contours, hierarchy = contours_generate(keynote_image)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        return_image = contour_outer_maskout(keynote_image, sorted_contours[1])
        return_image = cv2.drawContours(return_image, [sorted_contours[1]], -1, (255, 255, 255), 2)

        string = image_num_let_read(return_image)
        key_list.append(string)
    
    new_match_df = match_df.assign(key=pd.Series(key_list))
    return new_match_df


def keynote_pair_generate(
        source_img_path: str = None, 
        key_folder:str = None, 
        match_df_clean: DataFrame = None,  
        block_df: DataFrame = None):
    """
    Get the key-note pair in which the key is the figure and the note is the text.
    
    @param: img_path: path to the image.
    @param: key_folder: path to the folder to store the key images and the dict for the key-note pair.
    @param: filtered_match_contours: list containing filterd matching contours.
    @param: block_df: data frame containing filtered text blocks (paragraphs)
    @param: display_img_path: path to the display image, if None, set same as img_path.

    @return: display_image: image with all keys and notes circled out with rectangle.
    @return: key_note_pair: data frame containing key-note paire. This key-note pair is also saved.
    """
    source_image = cv2.imread(source_img_path)

    key_note_pair = DataFrame()
    text_block_done = []
    border = 4
    for i in range(len(match_df_clean)):
        contour = match_df_clean.iloc[i].contour
        (x, y, w, h) = cv2.boundingRect(contour)
        for j in range(len(block_df)):
            (bx, by, bw, bh, btext, bth) = block_df.iloc[j]
            if (bx > (x + w)) and (bx < (x + 2*w)) and ((by + bth//2) > y) and (by < (y + h)) and (bth > h//3) and (bw > w//2):
                if j not in text_block_done:
                    tmp = {"key": {"key_img": f"key{len(key_note_pair)}.png", "key_left": x, "key_top": y, "key_width": w, "key_height": h}, "note": dict(block_df.iloc[j])}
                    key_df = DataFrame([tmp])['key'].apply(lambda x: {} if pd.isna(x) else x).apply(pd.Series)[tmp['key'].keys()]
                    note_df = DataFrame([tmp])['note'].apply(lambda x: {} if pd.isna(x) else x).apply(pd.Series)[["text", "left", "top", "width", "height", "total_height"]]
                    contour_df = DataFrame([match_df_clean.iloc[i]]).reset_index(drop=True)
                    key_note_pair = pd.concat([key_note_pair, pd.concat([key_df, note_df, contour_df], axis=1)], ignore_index=True, sort=False)
                    text_block_done.append(j)
                    key_img = source_image[y-border:(y+h+border), x-border:(x+w+border), :]
                    cv2.imwrite(os.path.join(key_folder, key_note_pair.iloc[-1]['key_img']), key_img)
                break
    # save the key_note dataframe

    # sort the keynote in order top->bottom, left->right
    # 1. sort by x
    sorted_x = key_note_pair.sort_values("key_left").reset_index(drop=True)
    # 2. group by x, to deal with cases in which several columns exist
    list_start = [0]
    start_id = 0
    right_mark = sorted_x.iloc[0].left +  sorted_x.iloc[0].width
    for i in range(1, len(sorted_x)):
        if sorted_x.iloc[i].key_left > right_mark:
            right_mark = sorted_x.iloc[i].left + sorted_x.iloc[i].width
            start_id = i
            list_start.append(i)
        else:
            continue
    list_start.append(len(sorted_x))
    # 3. for each of the list_start, sort the sub list then combine
    sorted_y = DataFrame()
    for i in range(len(list_start)-1):
        start_id = list_start[i]
        end_id = list_start[i+1] - 1
        sub_df = sorted_x.loc[start_id:end_id]
        sub_sorted_y = sub_df.sort_values("key_top")
        sorted_y = pd.concat([sorted_y, sub_sorted_y], ignore_index=True, sort=False)
    sorted_y = sorted_y.reset_index(drop=True)

    # use the sorted data frame to save images
    for i in range(len(sorted_y)):
        orig_key_img = sorted_y.iloc[i].key_img
        new_key_img = f"key_{i+1}.png"
        sorted_y.at[i, "key_img"] = new_key_img
        os.rename(os.path.join(key_folder, orig_key_img), os.path.join(key_folder, new_key_img))
    
    # read the key 
    match_df = keynote_key_read(key_folder, sorted_y)
    # sorted_y.to_csv(f'{key_folder}/keynote.csv', index=False)
    # dataframe_save(sorted_y, f'{key_folder}/keynote.csv')
    dataframe_save(match_df, f'{key_folder}/keynote.csv')

    return match_df


def keynote_draw(
        info_json: dict = None, 
        display_image: np.array = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 2):
    """
    Box out the keynotes and their text.

    @param: info_json: dictionary containing information related to keynotes.
    @param: display_image: array of image to draw, usually using original siteplan image.
    @param: color: tuple of color.
    @param: thickness: thickness for drawing.

    @return: display_image_return: array of image with detected keynotes boxed out.
    """
    # box out the keynote and the text
    display_image_return = display_image.copy()
    border = 2
    # box out the title
    (x, y, w, th) = info_json["left"], info_json["top"], info_json["width"], info_json["total_height"]
    cv2.rectangle(display_image_return, (x-border, y-border), (x+w+border, y+th+border), color, thickness)
    # read in the data frame containing info of keynote pair
    df = pd.read_csv(os.path.join(info_json["key_folder"], "keynote.csv"))
    for i in range(len(df)):
        # draw box for the keynote
        kx = df.iloc[i].key_left
        ky = df.iloc[i].key_top
        kw = df.iloc[i].key_width
        kh = df.iloc[i].key_height
        cv2.rectangle(display_image_return, (kx-border, ky-border), (kx+kw+border, ky+kh+border), color, thickness)
        if thickness != -1:
            cv2.putText(display_image_return, f"key-{i+1}-{df.iloc[i].key}", (kx, ky-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness)

        # draw box for the text
        x = df.iloc[i].left
        y = df.iloc[i].top
        w = df.iloc[i].width
        h = df.iloc[i].total_height 
        cv2.rectangle(display_image_return, (x-border, y-border), (x+w+border, y+h+border), color, thickness)

    return display_image_return
