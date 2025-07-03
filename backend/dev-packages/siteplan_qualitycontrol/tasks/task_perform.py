"""
Functions for performing tasks.
"""
import os
from pathlib import Path
import json

from siteplan_qualitycontrol.utils import LogJson
from siteplan_qualitycontrol.tasks import KEY_MODULE_LIST


def single_module_perform(
        orig_img_path: str = None, 
        module_name: str = None, 
        process_log: LogJson = None):
    """
    Function to perform single module by module name. If a module is recorded as True in the log, the process will be passed.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    @param: module_name: string of module name.
    @param: process_log: LogJson file for the process log of the current siteplan page.
    """
    print(module_name)
    if not process_log.check(module_name):
        # if "pre" in KEY_MODULE_LIST.get(module_name).keys():
        #     module_func = KEY_MODULE_LIST.get(module_name).get("pre")
        #     module_func(orig_img_path)
        module_func = KEY_MODULE_LIST.get(module_name).get("main")
        module_func(orig_img_path)
        # if module_name == "keynote-gen":
        #     # for keynote-gen, extra information is needed
        #     keynote_template_name = module_config["keynote_template"]
        #     module_func(orig_img_path, keynote_template_name)
        # else:
        #     module_func(orig_img_path)
        process_log.update(module_name, True)
    else:
        print("already done")

    module_post = KEY_MODULE_LIST.get(module_name).get("post")
    if module_post:
        return_info = module_post(orig_img_path)
        for key in return_info.keys():
            print(f"{key} - {return_info[key]}")

# # old version
# def single_module_perform(
#         orig_img_path: str = None, 
#         module_name: str = None, 
#         process_log: LogJson = None, 
#         module_config: dict = None):
#     print(module_name)
#     if not process_log.check(module_name):
#         module_func = KEY_MODULE_LIST.get(module_name).get("main")
#         if module_name == "keynote-gen":
#             # for keynote-gen, extra information is needed
#             keynote_template_name = module_config["keynote_template"]
#             module_func(orig_img_path, keynote_template_name)
#         else:
#             module_func(orig_img_path)
#         process_log.update(module_name, True)
#     else:
#         print("already done")

#     module_post = KEY_MODULE_LIST.get(module_name).get("post")
#     if module_post:
#         return_info = module_post(orig_img_path)
#         for key in return_info.keys():
#             print(f"{key} - {return_info[key]}")

def loop_modul_perform(
        orig_img_path: str = None, 
        module_name: str = None, 
        process_log: LogJson = None, 
        total_length: int = None):
    """
    Function for perform loop module. This if for the keynote matching.

    @param: orig_img_path: string of path the originla PNG image for the siteplan.
    @param: module_name: name of the module.
    @param: total_length: number of length of the loop (total number of keynotes).
    """
    print(f"{module_name} - {total_length}")
    # do pre first
    module_pre = KEY_MODULE_LIST.get(module_name).get("pre")
    module_pre(orig_img_path)
    # perform loop 
    for index in range(total_length):
        print(f"keynote-{index+1}")
        # do main
        module_func = KEY_MODULE_LIST.get(module_name).get("main")
        module_func(orig_img_path, index)
        # do post
        module_post = KEY_MODULE_LIST.get(module_name).get("post")
        if module_post:
            return_info = module_post(orig_img_path, index)
            for key in return_info.keys():
                print(f"{key} - {return_info[key]}")


    