"""
Script containing functions for OCR tools.
"""

import cv2
import pytesseract
from pytesseract import Output
import pandas as pd
import numpy as np
from pandas import DataFrame
import re

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import contours_generate
from siteplan_qualitycontrol.images import number_template_match

def text_extract(
        image: np.array = None, 
        custom_config: str = r'--oem 3 --psm 11', 
        clean_conf_threshold: int = 10, 
        allowed_set: set = global_var.ALLOWED_CHARS):
    """
    Extract text from the input image then do clean up based on the detection confidence score and allowed charators.

    @param: image: numpy array containing the image for detection.
    @param: custom_config: configuration input for the pytesseract function.
    @param: clean_conf_threshold: detected text with "conf" score smaller than clean_conf_threshold will be removed.
    
    @return: df: {level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text}, dataframe containing all detect text information, both location and text. 
    """
    df = pytesseract.image_to_data(image, output_type=Output.DATAFRAME, config=custom_config)
    # clean based on the confidence score
    df.drop(df[df.conf<=clean_conf_threshold].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['text'] = df['text'].astype(str)
    # clean based on the global variable ALLOWED_CHARS
    orig_dtypes = df.dtypes
    for i in range(len(df)):
        (level, page, block, par, lin, word, x, y, w, h, conf, text) = df.iloc[i]
        text_set = set((text))
        if not text_set.issubset(allowed_set):
            df.loc[i] = None
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    # convert back to the original dtype
    for key in df.keys():
        df[key] = df[key].astype(orig_dtypes[key])
    
    return df


def block_extract(
        data_df: DataFrame = None):
    """
    Read in the data frame containing detected data of pytesseract.image_to_data and group them based on block_num.

    @param: data_df: {level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text}, dataframe containing all detect text information, both location and text. 

    @return: block_df: {left, top, width, height, text}, dataframe containing all detect text information, both location and text. 
    """
    block_text = {"left":[], "top":[], "width":[], "height":[], "text":[]}
    for block_num, words_per_block in data_df.groupby('block_num'):
        if not len(words_per_block):
            continue
        
        # deal with cases of misgrouping, especially for keynotes
        # the text in keynotes and the key notation are mistakely grouped with the text
        # differen these based on the heigh difference
        cut_loc = []
        heights = words_per_block.height.values
        tops = words_per_block.top.values
        for i in range(len(heights) - 1):
            gap = abs(heights[i] - heights[i+1])
            # add info about the location of the words
            top_gap = abs(tops[i]-tops[i+1])
            if (gap > np.array([heights[i], heights[i+1]]).min() * 0.5) or (top_gap > np.array([heights[i], heights[i+1]]).min() * 0.5):
                cut_loc.append(i)
            
        if len(cut_loc):
            cut_loc.append(len(heights))
            start = 0
            for end in cut_loc:
                words_per_block_sub = words_per_block.iloc[start:end+1]
                start = end + 1
                words = words_per_block_sub.text.values
                block = " ".join(words)

                word_boxes = []
                for left, top, width, height in words_per_block_sub[["left", "top", "width", "height"]].values:
                    word_boxes.append((left, top))
                    word_boxes.append((left+width, top+height))
                
                x, y, w, h = cv2.boundingRect(np.array(word_boxes))
                
                block_text['text'].append(block)
                block_text['left'].append(x)
                block_text['top'].append(y)
                block_text['width'].append(w)
                block_text['height'].append(h)
            continue

        words = words_per_block.text.values
        block = " ".join(words)

        word_boxes = []
        for left, top, width, height in words_per_block[["left", "top", "width", "height"]].values:
            word_boxes.append((left, top))
            word_boxes.append((left+width, top+height))

        x, y, w, h = cv2.boundingRect(np.array(word_boxes))
        
        block_text['text'].append(block)
        block_text['left'].append(x)
        block_text['top'].append(y)
        block_text['width'].append(w)
        block_text['height'].append(h)

    block_df = pd.DataFrame(block_text)

    return block_df

def block_extract_paragraph(
        block_df: DataFrame = None):
    """
    Read in the data frame containing results of group-based blocks and further group blocks as paragraphs.

    @param: block_df: {left, top, width, height, text}, dataframe containing all detect text information, both location and text. 

    @return: block_df: {left, top, width, height, text, total_height}, dataframe containing all detect text information after grouping, both location and text. 
    """
    # the block_extract function only have the block as line-wise
    # use this function to combine line-blocks which has in-line distacen less then the line height, these can seen as one paragraph
    def find_next(i, block_df):
        for j in range(len(block_df)):
            (xi, yi, wi, hi, texti, thi) = block_df.iloc[i]
            (xj, yj, wj, hj, textj, thj) = block_df.iloc[j]
            if (i != j) and ((yi+np.array([hi, hj]).min()+thi) > yj) and ((yi+thi) < yj):
            # if (i != j) and ((yi+hi+thi) > yj) and ((yi+thi) < yj):
                # line space is smaller than one line height
                if abs(xi - xj) < 10:
                    # block starter is close to each other (smaller than 10)
                    block_df.loc[i, 'left'] = np.array([xi, xj]).min()
                    block_df.loc[i, 'total_height'] = yj + hj - yi
                    block_df.loc[i, 'width'] = np.array([xi+wi, xj+wj]).max() - xi
                    block_df.loc[i, 'text'] = block_df.text[i] + ' ' + block_df.text[j]
                    block_df.loc[j, 'top'] = block_df.loc[j, 'left'] = block_df.loc[j, 'height'] = block_df.loc[j, 'width'] = block_df.loc[j, 'total_height'] = 0
                    block_df.loc[j, 'text'] = ''
                    find_next(j, block_df)
    
    block_df['total_height'] = block_df['height']
    for i in range(len(block_df)):
        find_next(i, block_df)

    # clean up, remove empty rows
    block_df = block_df[block_df['height']!=0].reset_index(drop=True)

    return block_df


def block_extract_part(
        block_df: DataFrame = None):
    """
    Read in the data frame containing results of group-based blocks and further group blocks as parts.

    @param: block_df: {left, top, width, height, text}, dataframe containing all detect text information, both location and text. 

    @return: block_df: {left, top, width, height, text, total_height}, dataframe containing all detect text information after grouping, both location and text. 
    """
    # the block_extract function only have the block as line-wise
    # use this function to combine line-blocks which has in-line distacen less then the line height, these can seen as one paragraph
    def find_next(i, block_df):
        for j in range(len(block_df)):
            (xi, yi, wi, hi, texti, thi) = block_df.iloc[i]
            (xj, yj, wj, hj, textj, thj) = block_df.iloc[j]
            if (i != j) and ((yi+hi+thi) > yj) and ((yi+thi) < yj):
                # line space is smaller than one line height
                if ((xi < (xj+wj//2)) and ((xi+wi) > (xj+wj//2))) or ((xj < (xi+wi//2)) and ((xj+wj) > (xi+wi//2))) or ((xi < xj) and ((xi+wi) > xj)):
                    # block starter is close to each other (smaller than 10)
                    block_df.loc[i, 'left'] = np.array([xi, xj]).min()
                    block_df.loc[i, 'total_height'] = yj + hj - yi
                    block_df.loc[i, 'width'] = np.array([xi+wi, xj+wj]).max() - xi
                    block_df.loc[i, 'text'] = block_df.text[i] + ' ' + block_df.text[j]
                    block_df.loc[j, 'top'] = block_df.loc[j, 'left'] = block_df.loc[j, 'height'] = block_df.loc[j, 'width'] = block_df.loc[j, 'total_height'] = 0
                    block_df.loc[j, 'text'] = ''
                    find_next(j, block_df)
    
    block_df['total_height'] = block_df['height']
    for i in range(len(block_df)):
        find_next(i, block_df)

    # clean up, remove empty rows
    block_df = block_df[block_df['height']!=0].reset_index(drop=True)

    return block_df


def ocr_draw(
        df: DataFrame = None, 
        display_image: np.array = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 2):
    """
    Read in data frames containing location information of detected text and draw box them out on image.

    @param: df: {left, top, width, height, text}, dataframe containing all detect text information, both location and text. 
    @param: display_image: numpy array containing image for draw boxes.
    @color: tuple of color, format BGR.
    @thickness: thickness for draw.

    @return: display_image_return: numpy array of image with all detected text boxed out.
    """
    # box out the detected text based on data frame
    # for each data frame, should contain left, top, width, height/total_height
    # copy to avoid change the original display image
    display_image_return = display_image.copy()
    for i in range(len(df)):
        x = df.iloc[i].left
        y = df.iloc[i].top 
        w = df.iloc[i].width
        if "total_height" in df.keys():
            h = df.iloc[i].total_height
        else:
            h = df.iloc[i].height
        cv2.rectangle(display_image_return, (x, y), (x + w, y + h), color, thickness)
    return display_image_return


def ocr_text_correction(
        image: np.array = None, 
        df: DataFrame = None):
    """
    Correctiong on the OCR text detection.

    @param: image: array of image.
    @param: df: dataframe containing OCR results on the input image.

    @return: df: dataframe of OCR results with correction.
    """
    for index in df.index:
        row = df.iloc[index]

        # this is for case if a / is detected by mistake, especially for cases when the numbers locate sparsely
        if "/" in row.text and row.text[-2:].upper() == "TH":
            df.at[index, "text"] = row.text.replace("/", "")
            # refresh row 
            row = df.iloc[index]

        # 3 can be misdetected as 5, so check all detect 5
        if "5" in row.text:
            (x, y, w, h) = (row.left, row.top, row.width, row.height)
            sub = image[y:y+h, x:x+w, :]
            contours, hierarcy = contours_generate(sub, 
                                                   thresh=127, 
                                                   mode=cv2.RETR_EXTERNAL, 
                                                   method=cv2.CHAIN_APPROX_NONE)
            outer_contours = []
            for i, c in enumerate(contours):
                if hierarcy[0, i, 3] == -1:
                    outer_contours.append(c)
            # sort from left to right
            sorted_outer_contours = sorted(outer_contours, key=lambda c: cv2.boundingRect(c)[0])
            # check text
            for j, char in enumerate(row.text):
                if char == "5":
                    n = number_template_match(sorted_outer_contours[j])
                    if n != "5":
                        df.at[index, "text"] = row.text[:j] + n + row.text[j+1:]
                        # refresh row 
                        row = df.iloc[index]

    return df


def string_loc_detect(
        data_df: DataFrame = None, 
        detect_string: str = None):
    """
    Read in data frame containing OCR results and return the rows that contain the desired string.

    @param: data_df: data frame containing OCR analysis results.
    @detect_string: string that need to be found.

    @detected_string_df: data frame of rows which text contain the desired string.
    """
    # get location information with string
    detected_string_df = DataFrame()
    for i in range(len(data_df)):
        text = data_df.iloc[i].text
        if detect_string in str(text):
            detected_string_df = pd.concat([detected_string_df, DataFrame([data_df.iloc[i]])], ignore_index=True, sort=False)

    return detected_string_df


def ocr_text_number_clean(
        df: DataFrame = None):
    """
    Clean everything other than number of OCR results.

    @param: df: dataframe containing OCR results.

    @param: return_df: dataframe containing only numbers (and .). 
    """
    return_df = df.copy()
    for index in return_df.index:
        number_text = re.sub(r'[^0-9.]', '', return_df.iloc[index].text).strip()
        return_df.at[index, "text"] = number_text

    return return_df


def ocr_text_signle_number_generate(
        df: DataFrame = None):
    """
    Detect only single number from OCR results.

    @param: df: dataframe containing OCR results.

    @return: out_number: final detected number.
    """
    out_number = df.iloc[0].text
    for index in np.arange(1, len(df), 1):
        # check empty or not, if not, check if end with . or next start with .
        if out_number != "":
            if df.iloc[index].text == "":
                return out_number
            if out_number[-1] == "." or df.iloc[index].text[0] == ".":
                out_number = out_number + df.iloc[index].text
                return out_number
        else:
            out_number = out_number + df.iloc[index].text

    return out_number