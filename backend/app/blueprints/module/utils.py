import os
from pathlib import Path
from flask import session, current_app
import time

from app.models import db, User, Session, Page
from siteplan_qualitycontrol.tasks import KEY_MODULE_LIST
from siteplan_qualitycontrol.utils import LogJson, ProjectConfigJson


def simple_module_perform(
        module_name: str = None):
    # orig_img_path = session["current_orig_img_path"]
    # get current user, project, and page
    # current_user = User.query.filter_by(email=session["current_user"]["email"]).first()
    # current_project = Project.query.filter_by(user_id=current_user.id, project_name=session["current_project"]["projectName"]).first()
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    # orig_img_path = session["current_orig_img_path"]
    session["current_orig_img_path"] = orig_img_path
    print(orig_img_path)
    # read in process log
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    # check if task is performed
    print(module_name)
    if not process_log.check(module_name):
        print(f"{module_name} - processing")
        module_func = KEY_MODULE_LIST.get(module_name).get("main")
        module_func(orig_img_path)
        process_log.update(module_name, True)
    else:
        print(f"{module_name} - already done")
        time.sleep(1)


def simple_module_post(
        module_name: str = None):
    # orig_img_path = session["current_orig_img_path"]
    # get current user, project, and page
    # current_user = User.query.filter_by(email=session["current_user"]["email"]).first()
    # current_project = Project.query.filter_by(user_id=current_user.id, project_name=session["current_project"]["projectName"]).first()
    current_page = Page.query.filter_by(session_id=session["currentSession"]["id"], page_number=session["currentPage"]).first()
    # from the current page, get the output folder for it
    orig_img_path = os.path.join(current_app.config["SERVER_FOLDER"], current_page.page_folder, "original.png")
    print(orig_img_path)
    session["current_orig_img_path"] = orig_img_path
    # read in process log
    process_log = LogJson(os.path.join(Path(orig_img_path).parent, "log.json"))

    # call for post func
    post_func = KEY_MODULE_LIST.get(module_name).get("post")

    if post_func is None:
        return_info = {"message": f"{module_name} done."}
    else:
        return_info = post_func(orig_img_path)

    return return_info
    