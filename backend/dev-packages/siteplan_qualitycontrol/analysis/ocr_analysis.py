"""
Perform OCR module.
"""
import os
import cv2
from pathlib import Path

from siteplan_qualitycontrol.basic import text_extract, block_extract, block_extract_paragraph, block_extract_part, ocr_draw

def body_ocr_analysis(
        orig_img_path: str = None, 
        custom_config: str = r'--oem 3 --psm 11', 
        clean_conf_threshold: int = 10):
    """
    Function to do ocr analysis on a given PNG image (body part).

    @param: img_path: path to the image, PNG format.
    """
    # display image for drawing
    display_image = cv2.imread(orig_img_path)
    # save folder path
    data_save_path = os.path.join(Path(orig_img_path).parent, "data")
    img_save_path = os.path.join(Path(orig_img_path).parent, "image")
    # read in the <body.png> for analysis, if not exist, do ocr on original image
    body_img_path = os.path.join(img_save_path, "body.png")
    if os.path.exists(body_img_path):
        image = cv2.imread(body_img_path)
    else:
        image = cv2.imread(orig_img_path)

    # text analysis
    data_df = text_extract(image=image, 
                           custom_config=custom_config, 
                           clean_conf_threshold=clean_conf_threshold)
    data_image = ocr_draw(data_df, display_image, (255, 0, 255), 2)
    data_df.to_csv(os.path.join(data_save_path, "data.csv"), index=False)
    cv2.imwrite(os.path.join(img_save_path, "data.png"), data_image)

    # data -> block
    block_df = block_extract(data_df)
    block_image = ocr_draw(block_df, display_image, (255, 0, 255), 2)
    block_df.to_csv(os.path.join(data_save_path, "block.csv"), index=False)
    cv2.imwrite(os.path.join(img_save_path, "block.png"), block_image)

    # block -> paragraph
    paragraph_df = block_extract_paragraph(block_df)
    paragraph_image = ocr_draw(paragraph_df, display_image, (255, 0, 255), 2)
    paragraph_df.to_csv(os.path.join(data_save_path, "paragraph.csv"), index=False)
    cv2.imwrite(os.path.join(img_save_path, "paragraph.png"), paragraph_image)

    # # block_to_part
    # part_df = block_extract_part(block_df)
    # part_image = ocr_draw(part_df, display_image, (255, 0, 255), 2)
    # part_df.to_csv(os.path.join(data_save_path, "part.csv"), index=False)
    # cv2.imwrite(os.path.join(img_save_path, "part.png"), part_image)