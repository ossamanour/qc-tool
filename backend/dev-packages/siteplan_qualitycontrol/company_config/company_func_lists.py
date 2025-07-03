"""
Dictionary for company name and their corresponding tool functions.
"""
from siteplan_qualitycontrol.company_config import hpd_landscape_sidebar_info_generate
from siteplan_qualitycontrol.company_config import hpd_landscape_body_sidebar_generate
from siteplan_qualitycontrol.company_config import hpd_landscape_template_call
from siteplan_qualitycontrol.company_config import hpd_scale_generate
from siteplan_qualitycontrol.company_config import hpd_landscape_template_path

from siteplan_qualitycontrol.company_config import seg_siteplan_sidebar_info_generate
from siteplan_qualitycontrol.company_config import seg_siteplan_body_sidebar_generate
from siteplan_qualitycontrol.company_config import seg_siteplan_template_call
from siteplan_qualitycontrol.company_config import seg_scale_generate
from siteplan_qualitycontrol.company_config import seg_siteplan_template_path

COMPANY_FUNC_LISTS = {
    "seg": {
        "info_generate": seg_siteplan_sidebar_info_generate, 
        "body_generate": seg_siteplan_body_sidebar_generate, 
        "template_call": seg_siteplan_template_call, 
        "scale_generate": seg_scale_generate, 
        "template_path": seg_siteplan_template_path,
    }, 
    "hpd": {
        "info_generate": hpd_landscape_sidebar_info_generate, 
        "body_generate": hpd_landscape_body_sidebar_generate, 
        "template_call": hpd_landscape_template_call, 
        "scale_generate": hpd_scale_generate, 
        "template_path": hpd_landscape_template_path,
    }
}