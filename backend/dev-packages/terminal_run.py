"""
Script to run the site plan quality control & cost estimate from the terminal end.
=> python terminal run  // run on any siteplan
=> python ternimal run -test    // run test mode, select from the pre-saved examples

Author: Ruolei Ji
"""

import os
import argparse

from siteplan_qualitycontrol.terminal_run import tool_select, file_choose, example_file_choose, config_setup
from siteplan_qualitycontrol.terminal_run import file_prepare_page_select
from siteplan_qualitycontrol.utils import ProjectConfigJson
from siteplan_qualitycontrol.terminal_run import quality_control_main, cost_estimate_main


# args
parser = argparse.ArgumentParser()
parser.add_argument("-test", action="store_true", help="Use test mode with examples.")
args = parser.parse_args()


def main():
    """
    Main function to run site plan quality control & cost estimate
    """
    # select quality control or cost estimate
    tool = tool_select()
    
    # choose file and set ouput folder
    if args.test:
        siteplan_pdf_path, save_path = example_file_choose()
    else:
        siteplan_pdf_path, save_path = file_choose()
    
    # set up config file
    config_path = os.path.join(save_path, "config.json")
    project_config = ProjectConfigJson(config_path=config_path)
    config_setup(tool=tool, config=project_config)

    # prepare file and select page
    orig_img_path = file_prepare_page_select(siteplan_pdf_path, save_path)

    # perform quality control or cost estimate based on choice before
    if tool == "Quality Control":
        quality_control_main(orig_img_path)
    else:
        cost_estimate_main(orig_img_path)


if __name__ == "__main__":
    main()