"""
Functions of tools for dimension quality control.
"""
import os
import cv2
import pandas as pd
from pandas import DataFrame, Series
import numpy as np

from siteplan_qualitycontrol.utils import distance, contour_connection_check
from siteplan_qualitycontrol.basic import text_extract, ocr_text_number_clean, ocr_text_signle_number_generate


def single_dimension_measure(
        arrow_tip1: Series = None, 
        arrow_tip2: Series = None, 
        scale_info: dict = None):
    """
    Given arrow tips (at two ends) of a dimension, measure it based on the detected scale ruler.

    @param: arrow_tip1: series containing information for the first arrow tip.
    @param: arrow_tip2: series containing information for the second arrow tip.
    @param: scale: list containing detecte scale ruler information.

    @return: dist: measured distance.
    """
    pt1 = arrow_tip1.tip_pt
    pt2 = arrow_tip2.tip_pt

    dist = distance(pt1, pt2) / scale_info["pixel_number"] * scale_info["scale_number"]

    return dist


def single_dimension_image_generate(
        arrow_tip1: Series = None, 
        arrow_tip2: Series = None, 
        original_image: np.array = None):
    """
    Crop the sub-image of the given two arrows.

    @param: arrow_tip1: series containing information for the first arrow tip.
    @param: arrow_tip2: series containing information for the second arrow tip.
    @param: original_image: array containing the original image

    @return: crop_img: cropped image. 
    @return: dst: rotated cropped image.
    """
    # get contours
    contour1 = np.array(arrow_tip1.contour)
    contour2 = np.array(arrow_tip2.contour)

    # mask out the dimension notation
    temp_original_image = original_image.copy()
    # get connection label
    label_results, label_region = contour_connection_check(contour1, contour2, temp_original_image, return_label=True)
    x, y, w, h = cv2.boundingRect(np.concat((contour1, contour2)))
    # use background color to mask out the dimension
    (y_list, x_list) = np.where(label_results==0)
    bg_color = temp_original_image[y+y_list[0], x+x_list[0], :]
    (y_list, x_list) = np.where(label_results==label_region)
    for i in range(len(x_list)):
        temp_original_image[y+y_list[i], x+x_list[i], :] = bg_color

    # generate the minAreaRect
    cntpt, (w, h), ang = cv2.minAreaRect(np.concat((contour1, contour2)))
    # expand the box to include the dimension mark 
    if w > h:
        h = h + 150
    else:
        w = w + 150
    new_rect = (cntpt, (w, h), ang)
    box = np.intp((cv2.boxPoints(new_rect)))

    # mask out everything outside the box
    mask = np.zeros_like(temp_original_image, np.uint8)
    cv2.fillPoly(mask, [box], (1, 1, 1))
    maskout_image = temp_original_image * mask + (1 - mask) * 255
    bx, by, bw, bh = cv2.boundingRect(box)
    sub_image = maskout_image[by:by+bh, bx:bx+bw]

    # expand the image to be square and rotate
    rows, cols = sub_image.shape[:2]
    row_border = max([0, (cols-rows)//2])
    col_border = max([0, (rows-cols)//2])
    sub_extend = cv2.copyMakeBorder(sub_image, row_border, row_border, col_border, col_border, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    # rotate
    angle1 = arrow_tip1.angle
    angle2 = arrow_tip2.angle

    rows, cols = sub_extend.shape[:2]
    if angle1 < 2:
        # this is to deal with vertical 
        M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), angle1-90, 1)
    else:
        M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), 90-angle1, 1)
    dst = cv2.warpAffine(sub_extend, M, (cols, rows), borderValue=(255, 255, 255))

    # # do text detection on the rotated image
    # data_df = text_extract(dst, custom_config=r'--oem 3 --psm 11')

    # instead of doing ocr on the whole sub image, use gradien of pixel intensity to crop the center part which contain the dimension number notation
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    # sum over column
    sum = gray.sum(axis=0) / gray.shape[0] / 255
    grad = np.gradient(sum)
    # take the indexes based on the abs-mean
    indexes = np.where(np.abs(grad) > np.mean(np.abs(grad)))[0]
    # if threshold larger than 0.02, use 0.02
    if np.mean(np.abs(grad)) > 0.02:
        indexes = np.where(np.abs(grad) > 0.02)[0]
    # take out the center part
    # assume all dimension notation locate at center of the line
    mid_loc = np.floor(len(grad) / 2)
    
    abs_diff = np.abs(indexes - mid_loc)
    min_index = np.argmin(abs_diff)

    dis = np.ceil(len(grad) / 10)
    for i in range(min_index-1, 0, -1):
        if indexes[i+1] - indexes[i] > dis:
            break
    start = indexes[i+1]
    for i in range(min_index+1, len(indexes), 1):
        if indexes[i] - indexes[i-1] > dis:
            break
    end = indexes[i]
    crop_img = dst[:, start:end+1, :]

    # # do ocr on the cropped image
    # crop_data_df = text_extract(crop_img, custom_config=r'--oem 3 --psm 11')

    return crop_img, dst


def single_dimension_read(
        crop_image: np.array = None, 
        image: np.array = None):
    """
    Read the number of a detected dimension.

    @param: crop_image: array containing cropped image of the detected dimension mark.
    @param: image: array containing original image.

    @return: readed number, 0 if no number is detected.
    @return: img_source: string of image source, None if no number detected.
    @return: tool_config: config used for ocr toll, None if no number dtected.
    """
    # get the number from crop image using psm 11
    data_df = text_extract(crop_image, custom_config=r'--oem 3 --psm 11')
    # clean up and get the final number
    if len(data_df) != 0:
        clean_data_df = ocr_text_number_clean(data_df)
        out_number = ocr_text_signle_number_generate(clean_data_df)
        if out_number != "":
            img_source = "crop_image"
            tool_config = r'--oem 3 --psm 11'
            return out_number.strip('.'), img_source, tool_config
    
    # if no number get from the crop image using psm 11, try psm 12
    data_df = text_extract(crop_image, custom_config=r'--oem 3 --psm 12')
    # clean up and get the final number
    if len(data_df) != 0:
        clean_data_df = ocr_text_number_clean(data_df)
        out_number = ocr_text_signle_number_generate(clean_data_df)
        if out_number != "":
            img_source = "crop_image"
            tool_config = r'--oem 3 --psm 12'
            return out_number.strip('.'), img_source, tool_config
    
    # if no number get from the crop image, try on image using psm 11
    data_df = text_extract(image, custom_config=r'--oem 3 --psm 11')
    # clean up and get the final number
    if len(data_df) != 0:
        clean_data_df = ocr_text_number_clean(data_df)
        out_number = ocr_text_signle_number_generate(clean_data_df)
        if out_number != "":
            img_source = "image"
            tool_config = r'--oem 3 --psm 11'
            return out_number.strip('.'), img_source, tool_config
        
    # if no number get from the image, try using psm 6
    data_df = text_extract(image, custom_config=r'--oem 3 --psm 6')
    # clean up and get the final number
    if len(data_df) != 0:
        clean_data_df = ocr_text_number_clean(data_df)
        out_number = ocr_text_signle_number_generate(clean_data_df)
        if out_number != "":
            img_source = "image"
            tool_config = r'--oem 3 --psm 6'
            return out_number.strip('.'), img_source, tool_config

    return 0, None, None


def dimension_check(
        dimension_arrow_pairs: dict = None, 
        arrow_angle_df: DataFrame = None, 
        scale_info: dict = None, 
        original_image: np.array = None, 
        tolerance: float = 0.05):
    """
    Measure the detected dimrnsions and check if the read dimension mark match the measured dimension number.

    @param: dimension_arrow_pairs: dictionary containing id of dimension arrow pairs.
    @param: arrow_angle_df: dataframe containing all arrow angle information.
    @param: scale_info: dictionary containing information of the detected scale ruler.
    @param: original_image: array of the original siteplan image.
    @param: tolerance: tolerance for the matching check.

    @return: dimension_qc_results_df: dataframe containing results of all dimension check.
    """
    # create a data frame to store all dimension qc results
    dimension_qc_results_df = DataFrame()

    # loop through all dimension pairs
    for key, val in dimension_arrow_pairs.items():
        arrow_tip1 = arrow_angle_df.iloc[int(key)]
        arrow_tip2 = arrow_angle_df.iloc[int(val)]

        # measure the dimension using scale
        measure_number = single_dimension_measure(arrow_tip1, arrow_tip2, scale_info)
        measure_number = float(measure_number)

        # read the dimension mark 
        crop_image, image = single_dimension_image_generate(arrow_tip1, arrow_tip2, original_image)
        read_number, img_source, tool_config = single_dimension_read(crop_image, image)
        read_number = float(read_number)

        # check if error is within tolerance
        if np.abs(measure_number - read_number) <= tolerance * measure_number:
            check = True
        else:
            check = False

        # save the results
        temp = {"arrow1": int(key), 
                "arrow2": int(val),
                "measure_num": measure_number, 
                "read_num": read_number, 
                "read_sourc": img_source, 
                "read_tool": tool_config, 
                "check": check}
        dimension_qc_results_df = pd.concat([dimension_qc_results_df, DataFrame([temp])], ignore_index=True, sort=False)

    return dimension_qc_results_df


def single_dimension_qc_draw(
        arrow_tip1: Series = None, 
        arrow_tip2: Series = None, 
        text: str = None, 
        display_image: np.array = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 2):
    """
    Draw the dimension quality control results on image for single dimension.

    @param: arrow_tip1: series for first arrow of dimension.
    @param: arrow_tip2: series for second arrow of dimension.
    @param: text: text to put on the siteplan image.
    @param: display_image: image to draw, use the original siteplan image.
    @param: color: tuple for color be to used.
    @param: thickness: thickness for drawing.

    @return: display_image_return: image with dimension quality control results drawn.
    """
    display_image_return = display_image.copy()

    # draw arrows and dimension
    contour1 = np.array(arrow_tip1.contour)
    contour2 = np.array(arrow_tip2.contour)
    cv2.drawContours(display_image_return, [contour1], -1, color, thickness)
    cv2.drawContours(display_image_return, [contour2], -1, color, thickness)
    pt1 = np.intp(np.array(arrow_tip1.mid_pt))
    pt2 = np.intp(np.array(arrow_tip2.mid_pt))
    cv2.line(display_image_return, pt1, pt2, color, thickness)

    # put text 
    cv2.putText(display_image_return, text, 
                (int((pt1[0]+pt2[0])/2), int((pt1[1]+pt2[1])/2)), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, color, thickness)

    return display_image_return


def dimension_qc_draw(
        dimension_qc_results_df: DataFrame = None, 
        display_image: np.array = None, 
        arrow_angle_df: DataFrame = None, 
        type: str = "A", 
        color: tuple = (255, 0, 255), 
        thickness: int = 2):
    """
    Draw all dimension quality control results on the siteplan image.

    @param: dimension_qc_results_df: dataframe containing results for dimension quality control.
    @param: display_image: image to draw, use the original siteplan image.
    @param: arrow_angle_df: dataframe containing information of all detected arrows.
    @param: type: string indicating what results to be drawn
    @param: color: tuple for color be to used.
    @param: thickness: thickness for drawing.

    @return: display_image_return: image with dimension quality control results drawn.
    """
    # "A" for all, "M" for measure number, "R" for read number
    display_image_return = display_image.copy()
    for index in dimension_qc_results_df.index:
        (idx1, idx2, measure_number, read_number, _, _, check) = dimension_qc_results_df.iloc[index]

        # first, draw all the arrows and dimension 
        arrow_tip1 = arrow_angle_df.iloc[idx1]
        arrow_tip2 = arrow_angle_df.iloc[idx2]
        

        if type == "M":
            text = f"{str(round(measure_number, 2))}(M)"
            display_image_return = single_dimension_qc_draw(arrow_tip1, arrow_tip2, text, display_image_return, color, thickness)
        elif type == "R":
            text = f"{str(read_number)}(R)"
            display_image_return = single_dimension_qc_draw(arrow_tip1, arrow_tip2, text, display_image_return, color, thickness)
        elif type == "A":
            if check == True:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            text = f"{str(read_number)}(R) - {str(round(measure_number, 2))}(M)"
            display_image_return = single_dimension_qc_draw(arrow_tip1, arrow_tip2, text, display_image_return, color, thickness)

    return display_image_return