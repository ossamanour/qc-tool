import os
from pathlib import Path
import inquirer
import json

from siteplan_qualitycontrol.images import list_keynote_template
from siteplan_qualitycontrol.utils import ProjectConfigJson, LogJson
from siteplan_qualitycontrol.tasks import KEYNOTE_MODULES
from siteplan_qualitycontrol.tasks import single_module_perform, loop_modul_perform
from siteplan_qualitycontrol.terminal_run import inquirer_list, inquirer_text


def keynote(
        orig_img_path: str = None, 
        process_log: LogJson = None):
    keynote_template_list = list_keynote_template()
    keynote_template = inquirer_list(
        "keynote_template", 
        message="Choose the keynote template", 
        choices=keynote_template_list)

    print(keynote_template)

    # read in the config file
    config_path = os.path.join(Path(orig_img_path).parents[1], "config.json")
    config = ProjectConfigJson(config_path)
    config.update("keynote_template", keynote_template)

    # perform all modules except the last matching module
    for module in KEYNOTE_MODULES[:-1]:
        single_module_perform(orig_img_path, module, process_log, config.config_json)

    # perform matching module
    # read in the keynote generate information and get the total number of keynotes
    with open(os.path.join(Path(orig_img_path).parent, "data", "keynote.json"), "r") as fp:
        information = json.load(fp)
    if information["status"] == "succeed":
        total_length = information["total_keynotes"]
    # perform match
    loop_modul_perform(orig_img_path, KEYNOTE_MODULES[-1], process_log, total_length)