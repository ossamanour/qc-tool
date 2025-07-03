"""
Functions used for company configure tools.
"""
import cv2
import numpy as np

from siteplan_qualitycontrol.utils import most_overlap_contour


def sub_image_mask_surround(orig_img, config, name):
    (x, y, w, h) = config[name]
    return_image = np.ones_like(orig_img) * 255
    return_image[y:y+h, x:x+w, :] = orig_img[y:y+h, x:x+w, :]
    return return_image


def sub_image_mask(orig_img, config, name):
    (x, y, w, h) = config[name]
    orig_img[y:y+h, x:x+w, :] = 255
    return orig_img


def contour_rect_mask_surround(orig_img, contour):
    return_image = np.ones_like(orig_img) * 255
    (x, y, w, h) = cv2.boundingRect(contour)
    return_image = np.ones_like(orig_img) * 255
    return_image[y:y+h, x:x+w, :] = orig_img[y:y+h, x:x+w, :]
    return return_image


def sub_image_get(
        image: np.array = None, 
        contours: list = None, 
        config: dict = None, 
        name: str = None, 
        threshold: float = 0.9, 
        get_full: bool = True):
    (x, y, w, h) = config[name]
    region = np.zeros_like(image)
    cv2.rectangle(region, (x, y), (x+w, y+h), 255, -1)

    chosen_contour = most_overlap_contour(contours, region, threshold=threshold)
    
    if get_full:
        return contour_rect_mask_surround(image, chosen_contour), chosen_contour
    else:
        (x, y, w, h) = cv2.boundingRect(chosen_contour)
        return image[y:y+h, x:x+w, :], chosen_contour