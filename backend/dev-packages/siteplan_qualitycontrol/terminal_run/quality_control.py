import os
from pathlib import Path
import inquirer

from siteplan_qualitycontrol.utils import LogJson
from siteplan_qualitycontrol.tasks import ZONING_MODULES, KEYNOTE_MODULES, DIMENSION_MODULES, PARKING_MODULES
from siteplan_qualitycontrol.tasks import single_module_perform
from siteplan_qualitycontrol.terminal_run import keynote, parking, height


def quality_control_main(
        orig_img_path: str = None):
    # load log file
    log_json_path = os.path.join(Path(orig_img_path).parent, "log.json")
    process_log = LogJson(log_json_path)

    # ask user to choose tasks
    tasks_list = ["ZONING", "DIMENSION", "KEYNOTE MATCH", "PARKING", "BUILDING HEIGHT"]
    questions = [
        inquirer.Checkbox(
            "tasks", 
            message="Choose the quality control tasks", 
            choices=tasks_list,
        ),
    ]
    answers = inquirer.prompt(questions)
    tasks = answers["tasks"]

    # task indenpend relationship
    if "PARKING" in tasks and "ZONING" not in tasks:
        tasks.append("ZONING")
    if "BUILDING HEIGHT" in tasks and "ZONING" not in tasks:
        tasks.append("ZONING")
    print(f"Performing quality control tasks: {tasks}.")

    ###################################################
    # ZONING                            
    ###################################################
    if "ZONING" in tasks:
        print("##########")
        print("Detecting Zoning ...")
        print("##########")
        for module in ZONING_MODULES:
            single_module_perform(orig_img_path, module, process_log)

    ###################################################
    # DIMENSION                            
    ###################################################
    if "DIMENSION" in tasks:
        print("##########")
        print("Performing Dimension Check ...")
        print("##########")
        for module in DIMENSION_MODULES:
            single_module_perform(orig_img_path, module, process_log)

    ###################################################
    # KEYNOTE MATCH                            
    ###################################################
    if "KEYNOTE MATCH" in tasks:
        print("##########")
        print("Performing Keynote Matching ...")
        print("##########")
        keynote(orig_img_path, process_log)

    ###################################################
    # PARKING                            
    ###################################################
    if "PARKING" in tasks:
        print("##########")
        print("Performing Parking Quality Control ...")
        print("##########")
        parking(orig_img_path, process_log)

    ###################################################
    # BUILDING HEIGHT                           
    ###################################################
    if "BUILDING HEIGHT" in tasks:
        print("##########")
        print("Checking Building Height Requirement ...")
        print("##########")
        height(orig_img_path, process_log)

    print("All selected tasks done.")