"""
Functions related to contours.
"""
import cv2
from pandas import DataFrame
import numpy as np
import math
from skimage.measure import label

from siteplan_qualitycontrol.utils import distance


def draw_contours_from_df(
        df: DataFrame = None, 
        display_image: np.array = None, 
        color: tuple = (255, 0, 255), 
        thickness: int = 2, 
        idx_mark: bool = True):
    """
    Read in the data frame and draw the contours.

    @param: df: data frame, may or may not contain a column named "contour".
    @param: display_image: numpy array containing images for draw.
    @param: color: tuple of color, format BGR.
    @param: thickness: thickness for draw.
    @param: idx_mark: boolean indicate if the index is marked, default as True.

    @return: display_image_return: numpy array of image with all contours draw.
    """
    # check, the data frame must contain a column named contour
    assert "contour" in df.keys(), "No column named 'contour' in input dataframe"
    display_image_return = display_image.copy()
    # go through all contours in the data frame
    for i in range(len(df)):
        contour = df.iloc[i].contour
        cv2.drawContours(display_image_return, [contour], -1, color, thickness)
        if idx_mark:
            # put index on 
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.putText(display_image_return, f"{i+1}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness)

    return display_image_return


def contour_connection_check(
        contour1: np.array = None, 
        contour2: np.array = None, 
        original_image: np.array = None, 
        return_label: bool = False):
    """
    Check if two contours on the same image is connected.

    @param: contour1: first contour.
    @param: contour2: second contour.
    @param: original_image: numpy array of the image.

    @return: connection: boolean variable indicates if the two contours are connected.
    """
    x, y, w, h = cv2.boundingRect(np.concat((contour1, contour2)))
    sub_image = original_image[y:y+h, x:x+w]

    sub_gray = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
    sub_thresh = cv2.threshold(sub_gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

    results = label(sub_thresh)
    
    global_label = np.zeros(original_image.shape[:2]).astype(np.int64)
    # global_label[y1:y2, x1:x2] = results
    global_label[y:y+h, x:x+w] = results

    contour1_labels = []
    for c1 in range(contour1.shape[0]):
        contour1_labels.append(global_label[contour1[c1].squeeze()[1], contour1[c1].squeeze()[0]])
    contour1_labels = np.array(contour1_labels)
    contour1_region = np.bincount(contour1_labels[contour1_labels!=0]).argmax()

    contour2_labels = []
    for c1 in range(contour2.shape[0]):
        contour2_labels.append(global_label[contour2[c1].squeeze()[1], contour2[c1].squeeze()[0]])
    contour2_labels = np.array(contour2_labels)
    contour2_region = np.bincount(contour2_labels[contour2_labels!=0]).argmax()

    if contour1_region == contour2_region:
        connection = True
        if return_label:
            return results, contour1_region
    else:
        connection = False
        if return_label:
            return None, None
    
    return connection


def rectangle_contour_search(
        contours: list = None, 
        epsilon_ratio: float = 0.01):
    """
    Functions to search rectangle through contours.

    @param: contours: list containing all detected contours of an image.
    @param: epsilon_ratio: epsilon for cv2.approxPolyDP function.

    @return: rectangle_id_list: list containing the id for all detected contours with rectangle shape.
    """
    rectangle_id_list = []
    
    for i, contour in enumerate(contours):
        # find the corners and keep on the shape with four corners
        eps = epsilon_ratio * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, eps, True)
        if approx.shape[0] == 4:
            # check if the 4-corner shape is a rectangle 
            # check if the two pairs of edge parallel
            angles = []
            for j in range(approx.shape[0]):
                pt1 = approx[j].squeeze()
                pt2 = approx[(j+1)%approx.shape[0]].squeeze()
                angle = math.degrees(math.atan2(pt1[0]-pt2[0], pt1[1]-pt2[1]))
                angles.append(angle)
            if np.abs(angles[0]-angles[2]) >= 178 and np.abs(angles[0]-angles[2]) <= 182 and np.abs(angles[1]-angles[3]) >= 178 and np.abs(angles[1]-angles[3]) <= 182:
                # temp = {"id": i, "contour": contour, "hierarchy": heirarchy[0][i, :], "approx": approx}
                # rectangle_contour_df = pd.concat([rectangle_contour_df, DataFrame([temp])], ignore_index=True, sort=False)
                rectangle_id_list.append(i)
    
    # return the rectangle contour id list
    return rectangle_id_list


def get_closest_contour(
        orig_loc: tuple = None, 
        df: DataFrame = None):
    """
    Given (x, y, w, h) of a contour, find the closed contour to it.

    @param: orig_loc: tuple of location information for the first contour, (x, y, w, h).
    @param: df: data frame contains location information of other contours, (left, top, width, height, ...).

    @return: (x, y, w, h) of the found contour.
    """
    distances = []
    (x, y, w, h) = orig_loc
    orig_pt = (x+w//2, y+h//2)
    for i in range(len(df)):
        (x, y, w, h) = (df.iloc[i].left, df.iloc[i].top, df.iloc[i].width, df.iloc[i].height)
        pt = (x+w//2, y+h//2)
        d = distance(orig_pt, pt)
        distances.append(d)

    closest_id = np.argmin(distances)
    closest_loc = (df.iloc[closest_id].left, df.iloc[closest_id].top, df.iloc[closest_id].width, df.iloc[closest_id].height)

    return closest_loc


def contour_outer_maskout(
        image: np.array = None, 
        contour: np.array = None, 
        fill_color: tuple = (255, 255, 255)):
    """
    Functions to mask everything outside the given contour.

    @param: image: array of input image.
    @param: contour: array of the input contour.
    @param: fill_color: tuple for the color to be used to fill the area.

    @return: return_image: array of the input image with everything outside the input contour masked out.
    """
    # mask out everything outside the contour
    stencil = np.zeros(image.shape[:-1]).astype(image.dtype)
    cv2.fillPoly(stencil, [contour], 255)
    sel = stencil != 255
    return_image = image.copy()
    return_image[sel] = fill_color

    return return_image

# def get_contour_all_intensities(
#         image: np.array = None, 
#         contour: np.array = None):
#     mask = np.zeros_like(image, )