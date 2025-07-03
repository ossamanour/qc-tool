import os
from pathlib import Path
import inquirer

from siteplan_qualitycontrol.utils import LogJson
from siteplan_qualitycontrol.tasks import single_module_perform
from siteplan_qualitycontrol.tasks import HDPAVEMENT_MODULES


def cost_estimate_main(
        orig_img_path: str = None):
    # load log file
    log_json_path = os.path.join(Path(orig_img_path).parent, "log.json")
    process_log = LogJson(log_json_path)
    
    # ask user to choose tasks
    tasks_list = ["HEAVY DUTY PAVEMENT"]
    questions = [
        inquirer.Checkbox(
            "tasks", 
            message="Choose the cost estimate tasks", 
            choices=tasks_list,
        )
    ]
    answers = inquirer.prompt(questions)
    tasks = answers["tasks"]

    print(f"Performing cost estimate tasks: {tasks}.")

    ###################################################
    # HEAVY DUTY PAVEMENT                           
    ###################################################
    if "HEAVY DUTY PAVEMENT" in tasks:
        print("##########")
        print("Heavy Duty Pavement ...")
        print("##########")
        for module in HDPAVEMENT_MODULES:
            single_module_perform(orig_img_path, module, process_log)

    print ("All selected tasks done.")
