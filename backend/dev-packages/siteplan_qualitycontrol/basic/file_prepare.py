"""
Script containing functions to do file prepare on siteplan PDF files.
"""

import os
from pathlib import Path
from pdf2image import convert_from_path
import cv2
import json
import numpy as np

from siteplan_qualitycontrol.utils import LogJson


def pdf2png(
        pdf_path: str = None, 
        save_path: str = None, 
        dpi: int = 300):
    """
    Convert all pages in the pdf file into images and save.
    Create a folder under {img_save_path} with the pdf file name and page number {pdf_name.pi} will be created and the converted image will be saved as {original.png}.
    A {log.json} file is also created for process log of the current file.
    Results folder {data} and {images} are created to store results.

    @param: pdf_path: path to the source pdf file.
    @param: img_save_path: path to the location to save the converted images.
    @param: dpi: dpi value for convert_from_path() function, control the image quality

    @return: page_num: total page number 
    """
    print("aa")
    # convert pdf pages to images
    pages = convert_from_path(pdf_path, dpi=dpi)
    # save the converted pages
    for i, page in enumerate(pages):
        print(i)
        page_save_path = os.path.join(save_path, f"p{i+1}")
        os.makedirs(page_save_path, exist_ok=True)
        page.save(os.path.join(page_save_path, "original.png"))
        ## prepare log file and resutls folders
        # create a log file for each page
        process_log = LogJson(os.path.join(page_save_path, "log.json"))
        if not process_log.check("pdf2png"):
            process_log.update("pdf2png", True)
        # create save folders for images and data
        data_save_path = os.path.join(page_save_path, "data")
        os.makedirs(data_save_path, exist_ok=True)
        img_save_path = os.path.join(page_save_path, "image")
        os.makedirs(img_save_path, exist_ok=True)
    page_num = i + 1
    return page_num


def pdf_img_prepare(
        pdf_path: str = None, 
        save_path: str = None, 
        dpi: int = 300):
    """
    Prepare the site plan PDF file, including converting to PNG image, and create basic information json file for later use.
    A {prepare_log.json} file is created to log if the file prepare is already done.

    @param: pdf_path: path to the source pdf file.
    @parem: save_path: path to the location to save all analysis results.
    @param: dpi: dpi value for convert_from_path() function, control the image quality
    
    @return: page_num: total page number.
    """
    # check if the file parepare is already donw
    if os.path.exists(os.path.join(save_path, "prepare_log.json")):
        with open(os.path.join(save_path, "prepare_log.json"), "r") as fp:
            note = json.load(fp)
            page_num = note["page_num"]
            file_prepare = note["file_prepare"]
            # check if file is already prepared
            if file_prepare:
                return page_num
    
    page_num = pdf2png(pdf_path, save_path, dpi)
    # create the prepare log file
    note = {"file_prepare": True, "page_num": page_num}
    with open(os.path.join(save_path, "prepare_log.json"), "w") as fp:
        json.dump(note, fp, indent=4)

    return page_num