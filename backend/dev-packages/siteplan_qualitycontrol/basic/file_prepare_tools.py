"""
Functions of tools for PDF file preparation.
"""
import os
from pathlib import Path
from pdf2image import convert_from_path
import json
from PyPDF2 import PdfReader, PdfWriter

from siteplan_qualitycontrol.utils import LogJson


def split_pdf(
        pdf_path: str = None, 
        save_path: str = None):
    """
    Split one multiple-page PDF file to seperate PDF files each with only one page.

    @param: pdf_path: path to the PDF file.
    @param: save_path: path to the folder where to save the seperate PDF files.

    @return: page_num: number of total pages in the input PDF file.
    """
    # read in pdf file
    input = PdfReader(open(pdf_path, "rb"))

    # save each page
    page_num = len(input.pages)
    for i in range(page_num):
        output = PdfWriter(input.pages[i])
        output.add_page(input.pages[i])
        output_folder = os.path.join(save_path, f"p{i+1}")
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "original.pdf")
        with open(output_file, "wb") as outputStream:
            output.write(outputStream)
    
    # return total page
    return page_num


def pdf2png(
        pdf_path: str = None, 
        save_path: str = None, 
        dpi: int = 300):
    """
    Convert PDF files to PNG image.

    @param: pdf_path: path to the PDF file.
    @param: save_path: path to folder where to save the generated PNG file.
    @param: dpi: dpi parameter for the convert.

    @return: page_number: total number of pages in 
    """
    # split multi-page pdf to single-page pdf
    # this step is to solve the memory shortage problem for large pdf files
    page_num = split_pdf(pdf_path, save_path)

    # pdf -> image
    for i in range(page_num):
        single_page_path = os.path.join(save_path, f"p{i+1}", "original.pdf")
        # convert to image
        page = convert_from_path(single_page_path, dpi=dpi)
        # save image
        page_save_path = os.path.join(save_path, f"p{i+1}")
        page[0].save(os.path.join(page_save_path, "original.png"))
        # create a log file for each page
        process_log = LogJson(os.path.join(page_save_path, "log.json"))
        if not process_log.check("pdf2png"):
            process_log.update("pdf2png", True)
        # create save folders for images and data
        data_save_path = os.path.join(page_save_path, "data")
        os.makedirs(data_save_path, exist_ok=True)
        img_save_path = os.path.join(page_save_path, "image")
        os.makedirs(img_save_path, exist_ok=True)

    return page_num


def pdf_image_prepare(
        pdf_path: str = None, 
        save_path: str = None, 
        dpi: int = 300):
    # check if the file parepare is already done
    if os.path.exists(os.path.join(save_path, "prepare_log.json")):
        with open(os.path.join(save_path, "prepare_log.json"), "r") as fp:
            note = json.load(fp)
            page_num = note["page_num"]
            file_prepare = note["file_prepare"]
            # check if file is already prepared
            if file_prepare:
                return page_num
            
    # convert to images
    page_num = pdf2png(pdf_path, save_path, dpi)

    # create the prepare log file
    note = {"file_prepare": True, "page_num": page_num}
    with open(os.path.join(save_path, "prepare_log.json"), "w") as fp:
        json.dump(note, fp, indent=4)

    return page_num
