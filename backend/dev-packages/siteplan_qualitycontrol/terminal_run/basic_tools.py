import os
from pathlib import Path
import inquirer
import tkinter as tk
from tkinter import filedialog

from siteplan_qualitycontrol.utils import global_var
from siteplan_qualitycontrol.utils import ProjectConfigJson
from siteplan_qualitycontrol.ce_basic import list_all_price_sheet_templates
from siteplan_qualitycontrol.basic import pdf_image_prepare
from siteplan_qualitycontrol.terminal_run import inquirer_list, inquirer_text


SITEPLAN_PDF_TEST_EXAMPLES = {
    00: "test/02 Exhibit 4 - Preliminary Site Plan Set.pdf",
    10: "Avalon Development/Whataburger - Avondale - NEC McDowell Rd & 107th Ave - 201015/SUBMITTALS & QC/2021-12-15 1st Site Plan-DR to City/8. Site Plan.pdf", 
    11: "Avalon Development/Whataburger - Avondale - NEC McDowell Rd & 107th Ave - 201015/SUBMITTALS & QC/2021-12-15 1st Site Plan-DR to City/9. Landscape Plan.pdf",
    20: "Barclay/Angie's Lobsters - Gilbert - SWC Gilbert & Baseline - 210526/8 SUBMITTALS & QC/2022-05-19 1st DR to Town/05 Site Plan.pdf", 
    21: "Barclay/Angie's Lobsters - Gilbert - SWC Gilbert & Baseline - 210526/8 SUBMITTALS & QC/2022-05-19 1st DR to Town/06 Preliminary Landscape Plan.pdf", 
    30: "Barclay/EOS - Tempe - 750 E. Guadalupe - 220523/8 SUBMITTALS & QC/2022-11-11- Site to City/03 Site Plan.pdf",
    # 31: "",
    40: "Floor & Decor/Scottsdale - 15515 N. Hayden Rd - 230311/8  SUBMITTALS & QC/2023-06-27 DR Application#1(Client)/24. Site Plan.pdf",
    41: "Floor & Decor/Scottsdale - 15515 N. Hayden Rd - 230311/8  SUBMITTALS & QC/2023-06-27 DR Application#1(Client)/33. Preliminary Landscape Plan.pdf",
    50: "Fry's/Frys 56 - Peoria - NEC W. Olive Ave & 83rd Ave - 220811/8 SUBMITTALS & QC/2023-05-30 Site  Plan to City/06 Conceptual Site Plan.pdf", 
    51: "Fry's/Frys 56 - Peoria - NEC W. Olive Ave & 83rd Ave - 220811/8 SUBMITTALS & QC/2023-05-30 Site  Plan to City/07 Conceptual Landscape Plan.pdf", 
    60: "Fry's/Frys 104 FC Flagstaff 200402/8 SUBMITTALS & QC/2020-10-26- Site Plan to City via Email #2/II.1 - Site Plan.pdf", 
    61: "Fry's/Frys 104 FC Flagstaff 200402/8 SUBMITTALS & QC/2020-10-26- Site Plan to City via Email #2/II.4 - Landscape Plan.pdf",
    70: "Fry's/Frys 655 - Gilbert - Morrison Ranch - Power & Elliot - 210317/8 SUBMITTALS & QC/2023-05-25 Admin Rev.- Site Plan #2/02 Exhibit 4 - Preliminary Site Plan Set.pdf", 
    # 70: "Fry's/Frys 655 - Gilbert - Morrison Ranch - Power & Elliot - 210317/10 LATEST PLANS/10.2 - Construction Plans/210317-CD-C2.00-C2.12.pdf", 
    71: "Fry's/Frys 655 - Gilbert - Morrison Ranch - Power & Elliot - 210317/8 SUBMITTALS & QC/2023-05-25 Admin Rev.- Site Plan #2/03 Exhibit 5 - Preliminary Landscape Plan.pdf",
    80: "Mark Development, Inc/Frys FC #11 - Glendale - SWC Montebello Ave & 67th Ave - 221219/8 SUBMITTALS & QC/2023-09-15 Site Plan #1/03. Preliminary Site Plan.pdf",
    81: "Mark Development, Inc/Frys FC #11 - Glendale - SWC Montebello Ave & 67th Ave - 221219/8 SUBMITTALS & QC/2023-09-15 Site Plan #1/08. Preliminary Landscape Plan.pdf", 
    90: "Maverik/Eloy, AZ - FC - SWC I-10 & Sunshine Blvd - 230717/8 SUBMITTALS & QC/2023-09-26 Site Plan/08 Preliminary Development Plan.pdf",
    91: "Maverik/Eloy, AZ - FC - SWC I-10 & Sunshine Blvd - 230717/8 SUBMITTALS & QC/2023-09-26 Site Plan/08 Preliminary Landscape Plan.pdf",
    100: "Whataburger/Phoenix - NEC 25th & Baseline - 220629/8 SUBMITTALS & QC/2022-12-02 Minor Site Plan/05b C2.10 Site Plan.pdf",
    101: "Whataburger/Phoenix - NEC 25th & Baseline - 220629/8 SUBMITTALS & QC/2023-09-14 Landscape T126071-LSPL/05b L1.0 Landscape Plan.pdf"}


def example_file_choose():
    example = inquirer_list(
        "example", 
        message="Choose the test example you want", 
        choices=list(SITEPLAN_PDF_TEST_EXAMPLES.values()))
    data_folder = os.path.join(Path(global_var.ROOT).parents[1], "data", "PROJECTS")
    siteplan_pdf_path = os.path.join(data_folder, example)

    print(f"Performing on Example: \n -> {example}")

    questions = [
        inquirer.Text(
            "save_folder", 
            message="Where do you want to save?", 
            default="output_example"
        )
    ]
    answers = inquirer.prompt(questions)
    save_folder = answers["save_folder"]
    # default save folder will be output_example under the data folder
    save_folder = os.path.join(Path(global_var.ROOT).parents[1], "data", save_folder)
    out_folder = os.path.join(*siteplan_pdf_path[siteplan_pdf_path.find("PROJECTS")+9:].split("/")[:-1], siteplan_pdf_path[siteplan_pdf_path.find("PROJECTS"):].split("/")[-1].replace(".pdf", ""))
    save_path = os.path.join(save_folder, out_folder)
    os.makedirs(save_path, exist_ok=True)

    print(f"All results will be saved to \n -> {save_path}")
    return siteplan_pdf_path, save_path


def file_choose():
    # ask for input file
    print("Choose the input site plan PDF file: ")
    root = tk.Tk()
    root.withdraw()
    siteplan_pdf_path = filedialog.askopenfilename()

    print(f"Performing on File: \n -> {siteplan_pdf_path}")

    # ask for save folder
    # set default as the same directory with the original 
    # or user can choose a new folder on their own choice
    default_save_folder = os.path.join(Path(siteplan_pdf_path).parent, f"SP-terminal-{Path(siteplan_pdf_path).stem}")
    save_path = inquirer_list(
        "save_path", 
        message="Where do you want to save (Default or Ohters)?", 
        choices=[default_save_folder, "Others"])
    if save_path == "Others":
        print("Choose the folder to save the results:")
        save_path = filedialog.askdirectory()
    else:
        save_path = default_save_folder
        os.makedirs(save_path, exist_ok=True)

    print(f"All results will be saved to \n -> {save_path}")
    return siteplan_pdf_path, save_path


def tool_select():
    print("AIAEC")
    tool = inquirer_list(
        "tool", 
        message="Do you want to perform Quality Control or Cost Estimate", 
        choices=["Quality Control", "Cost Estimate"])

    return tool


def config_setup(
        tool: str = None, 
        config: ProjectConfigJson = None):
    company = inquirer_list(
        "company", 
        message="Choose the company make the site plan / landscape paln.", 
        choices=["SEG", "HPD"])
    config.update("company", company.lower())

    if tool == "Cost Estimate":
        price_sheet_list = list_all_price_sheet_templates()
        price_sheet = inquirer_list(
            "price_sheet", 
            message="Choose price sheet template for cost estimate", 
            choices=price_sheet_list)
        config.update("price_sheet", price_sheet)
        

def file_prepare_page_select(
        siteplan_pdf_path: str = None, 
        save_path: str = None):
    print("Loading File ...")
    total_page = pdf_image_prepare(pdf_path=siteplan_pdf_path, 
                                   save_path=save_path, 
                                   dpi=300)
    
    # choose if there are multiple pages
    pages = [f"p{i+1}" for i in range(total_page)]
    page = inquirer_list(
        "page", 
        message="Choose the page to perform tasks", 
        choices=pages)
    orig_img_path = os.path.join(save_path, page, "original.png")

    return orig_img_path

