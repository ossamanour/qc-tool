"""
Functions related to OpenCV.
"""
import cv2
import numpy as np
import pandas as pd
from pandas import DataFrame


def contours_generate(
        image: np.array = None, 
        thresh: int = 127,
        type: int = cv2.THRESH_BINARY_INV, 
        mode: int = cv2.RETR_CCOMP, 
        method: int = cv2.CHAIN_APPROX_SIMPLE):
    """
    Generate contours from an input image (array).

    @param: image: Numpy array store an image, format as BGR.
    @param: thresh: threshold for cv2.threshold.
    @param: type: type for cv2.threshold.
    @param: mode: mode for cv2.findContours.
    @param: method: method for cv2.findContours.

    @return: contours: list containing detected contours.
    @return: hierarchy: list containing detected hierarchy.
    """
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image_gray, thresh, 255, type)
    contours, hierarchy = cv2.findContours(thresh, mode, method)

    return contours, hierarchy

def approx_poly(
        contours: list = [], 
        n: int = 4,
        epsilon_ratio: float = 0.04):
    """
    Contour approximation with edge number of (n).

    @param: contours: list containing detected contours of an image.
    @param: n: number of corners for approx poly detection.
    @param: epsilon_ratio: epsilon param for cv2.approxPolyDP.

    @return: return_contours: list containing all selected contours.
    """
    return_contours = []
    for contour in contours:
        epsilon = epsilon_ratio * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == n:
            return_contours.append(contour)
    return return_contours


def image_view(
        image: np.array = None,
        window_name: str = "test"):
    """
    Function to view an image (array).

    @param: image: Numpy array containing an image, format as BGR.
    @param: window_name: name for the pop-up window.
    """
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def most_overlap_contour(
        contours: list = None, 
        region: np.array = None, 
        threshold: float = 0.9):
    """
    Function to find the contours that overlap with the given region, most overlap.

    @param: contours: list containing all detected contours of an image.
    @param: region: 
    @param: threshold: 

    @return: chosen_contour: contour what overlap with given region the most.
    """
    # print("start")
    region_area = np.logical_and(region, region).sum()
    # print(region_area)
    # sort the contours based on area
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # star with the region area
    region_non_overlap = region_area
    c_non_overlap = region_area
    # go through all contours and check the overlap area
    for c in sorted_contours:
        contour_mask = np.zeros_like(region)
        cv2.drawContours(contour_mask, [c], 0, 255, -1)
        overlap = np.logical_and(region, contour_mask).sum()
        c_area = np.logical_and(contour_mask, contour_mask).sum()

        # break out of the loop if area is less than 90% of the region
        if c_area < threshold * region_area:
            break

        # check the error of of non-overlap area and take the one that has the least
        # the non-overlap check should done for both the region area and the contour area
        # print(overlap - region_area)
        if overlap > 0: 
            if np.abs(overlap - region_area) < np.abs(region_non_overlap):
                # print("chosen")
                region_non_overlap = np.abs(overlap - region_area)
                chosen_contour = c
            if np.abs(overlap - c_area) < np.abs(c_non_overlap):
                # print("c chose")
                c_non_overlap = np.abs(overlap - c_area)
                chosen_contour = c
        
    return chosen_contour


def match_template(
        image: np.array = None, 
        template: np.array = None, 
        thresh: int = 127, 
        type: int = cv2.THRESH_BINARY, 
        match_threshold: float = 0.9):
    """
    Function to do template matching on image.

    @param: image: array of image in format BGR.
    @param: template: array of template in format BGR.
    @param: thresh: thresh for image preprocessing.
    @param: type: type for image preprocessing.
    @param: match_threshold: threshold for the template matching.

    @return: match_df: dataframe containing all find matching contours.
    """
    # image preprocessing
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image_thresh = cv2.threshold(image_gray, thresh, 255, type)

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    _, template_thresh = cv2.threshold(template_gray, thresh, 255, type)

    (tH, tW) = template.shape[:2]

    # template match, saved in data frame
    # template match
    match_df = DataFrame()
    result = cv2.matchTemplate(image_thresh, template_thresh, cv2.TM_CCOEFF_NORMED)

    (yCoords, xCoords) = np.where(result >= match_threshold)

    # add mask to remove duplicates
    mask = np.zeros(image.shape[:2], np.uint8)
    for (x, y) in zip(xCoords, yCoords):
        if mask[y+tH//2, x+tW//2] != 255:
            mask[y:y+tH, x:x+tW] = 255
            tmp = {"left": [x], "right": [y], "width": [tW], "height": [tH], "score": [result[y, x]]}
            match_df = pd.concat([match_df, DataFrame.from_dict(tmp)], ignore_index=True, sort=False)
            
    return match_df


def distance(pt1, pt2):
    """
    Calculate distance between two points.
    """
    return ((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**0.5

