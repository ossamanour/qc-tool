"""
List of [module_name - module function] and [task - module].
"""
from siteplan_qualitycontrol.analysis import body_sidebar_generate, body_ocr_analysis 
from siteplan_qualitycontrol.analysis import information_generate, information_post 
from siteplan_qualitycontrol.analysis import zoning_information_generate, zoning_post
from siteplan_qualitycontrol.analysis import keynote_generate, keynote_generate_post
from siteplan_qualitycontrol.analysis import keynote_match_pre, keynote_match, keynote_match_post
from siteplan_qualitycontrol.analysis import arrow_generate, arrow_generate_post
from siteplan_qualitycontrol.analysis import dimension_generate, dimension_generate_post
from siteplan_qualitycontrol.analysis import scale_generate, scale_post
from siteplan_qualitycontrol.quality_control import dimension_quality_control, dimension_quality_control_post
from siteplan_qualitycontrol.analysis import parking_count, parking_count_post
from siteplan_qualitycontrol.cost_estimate import cost_estimate_prepare
from siteplan_qualitycontrol.cost_estimate import heavyduty_pavement, heavyduty_pavement_post
from siteplan_qualitycontrol.cost_estimate import fire_hydrant, fire_hydrant_post
from siteplan_qualitycontrol.cost_estimate import light_pole, light_pole_post
from siteplan_qualitycontrol.cost_estimate import ada_ramp, ada_ramp_post
from siteplan_qualitycontrol.cost_estimate import ada_sign, ada_sign_post
from siteplan_qualitycontrol.cost_estimate import trash_rack, trash_rack_post


KEY_MODULE_LIST = {
    "body-sidebar": {"main": body_sidebar_generate, 
                     "post": None}, 
    "body-ocr": {"main": body_ocr_analysis, 
                 "post": None}, 
    "info-gen": {"main": information_generate,
                 "post": information_post}, 
    "zoning": {"main": zoning_information_generate, 
               "post": zoning_post}, 
    "keynote-gen": {"main": keynote_generate, 
                    "post": keynote_generate_post},
    "keynote-match-pre": {"main": keynote_match_pre, 
                          "post": None},
    "keynote-match": {"main": keynote_match, 
                      "post": keynote_match_post}, 
    "arrow-gen": {"main": arrow_generate, 
                  "post": arrow_generate_post}, 
    "dimension-gen": {"main": dimension_generate, 
                      "post": dimension_generate_post}, 
    "scale-gen": {"main": scale_generate, 
                  "post": scale_post}, 
    "dimension-qc": {"main": dimension_quality_control, 
                     "post": dimension_quality_control_post}, 
    "parking-count": {"main": parking_count, 
                      "post": parking_count_post}, 
    "costestimate-prepare": {"main": cost_estimate_prepare, 
                             "post": None},
    "heavyduty-pavement": {"main": heavyduty_pavement, 
                          "post": heavyduty_pavement_post}, 
    "fire-hydrant": {"main": fire_hydrant, 
                     "post": fire_hydrant_post}, 
    "light-pole": {"main": light_pole, 
                   "post": light_pole_post},
    "ada-ramp": {"main": ada_ramp, 
                 "post": ada_ramp_post},
    "ada-sign": {"main": ada_sign, 
                 "post": ada_sign_post},
    "trash-rack": {"main": trash_rack, 
                   "post": trash_rack_post}
}

ZONING_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "info-gen", 
    "zoning"
]

KEYNOTE_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "keynote-gen",
    "keynote-match-pre",  
    "keynote-match"
]

DIMENSION_MODULES = [
    "body-sidebar",
    "body-ocr",  
    "arrow-gen", 
    "dimension-gen", 
    "scale-gen", 
    "dimension-qc"
]

PARKING_MODULES = [
    "body-sidebar",
    "body-ocr",
    "parking-count"
]


# Cost Estimate
HDPAVEMENT_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "scale-gen",
    "costestimate-prepare",
    "heavyduty-pavement"
]

FIREHYDRANT_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "keynote-gen",
    "keynote-match-pre", 
    "costestimate-prepare",
    "fire-hydrant"
]

LIGHTPOLE_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "keynote-gen",
    "keynote-match-pre", 
    "costestimate-prepare",
    "light-pole"
]

ADARAMP_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "keynote-gen",
    "keynote-match-pre", 
    "costestimate-prepare",
    "ada-ramp"
]

ADASIGN_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "keynote-gen",
    "keynote-match-pre", 
    "costestimate-prepare",
    "ada-sign"
]

TRASHRACK_MODULES = [
    "body-sidebar", 
    "body-ocr", 
    "keynote-gen",
    "keynote-match-pre", 
    "costestimate-prepare",
    "trash-rack"
]


