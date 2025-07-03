"""
Functions for converting string to math expressions.
"""

import os
from pathlib import Path
import pandas as pd
import re
import math


def is_number(s):
    """
    Reutrn True if the input string contains only number(s).
    """
    return bool(re.fullmatch(r'[-+]?\d+(\.\d+)?', s))

def contain_no_number(s):
    """
    Return True if the input string contains NO number.
    """
    contain_number = any(c.isnumeric() for c in s)
    return not contain_number

def string_to_formula_basic(
        statement: str = None):
    """
    Read in a string containing description of a formula to calculate the minimum parking requirement, return a list of required parameters.
    All math symbols: +, -, *, /, (, ), MUST have space on both side to be distinguished from parameter description.

    @param: statement: string containing formula.

    @return: p_clean_list: list containing strings represent the required parameters. 
    """
    # for each formula string, separate the string into list of parameters
    # symbo used to separate: +, -, *, /, (, ).
    statement = statement.strip()
    if not pd.isna(statement):
        p_list = []
        start = 0
        for end in range(len(statement) - 3):
            if statement[end:end+3] in (" + ", " - ", " * ", " / ", " ( ", " ) "):
                p_list.append(statement[start:end])
                start = end + 3
        p_list.append(statement[start:])
    else:
        p_list = []

    # eliminate params of empty string and numbers
    # instead of check for numeric, need to check decimal
    
    p_clean_list = []
    for p in p_list:
        if is_number(p) or len(p) == 0 or p in p_clean_list:
            pass
        else:
            p_clean_list.append(p)
    # delete duplicates
    # p_clean_list = list(set(p_clean_list))

    return p_clean_list


def string_to_formula(
        statement: str = None):
    """
    Read in a string containing description of a formula to calculate the minimum parking requirement, return a list of required parameters.
    All math symbols: +, -, *, /, (, ), MUST have space on both side to be distinguished from parameter description.
    This function can also deal with statements of `min()` and `max()` cases.
    Details of how the statement is formed please refer to the `furmula_rule.md`.

    @param: statement: string containing formula.

    @return: p_clean: list containing strings represent the required parameters. 
    @return: statement: statements that are modified (for `min/max` case, statements needs to be modified).
    """
    # 1. +, -, *, /, (): all operation symbols MUST have space on both sides
    # 2. min(): MIN statement1 : statement2
    # 3. max(): MAX statement1 : statement2
    # statement1 and statement2 are simple statements same as case 1.
    
    # MIN or MAX must be at the begining to be identified
    if statement[:3] == "MIN" or statement[:3] == "MAX":
        # separate the original statement into two
        loc = statement.find(" : ")
        statement1 = statement[4: loc]
        statement2 = statement[loc+3:]

        # deal with each statement and get the final parameter list
        p_list1 = string_to_formula_basic(statement1)
        p_list2 = string_to_formula_basic(statement2)
        p_list = p_list1 + p_list2

        # modify the statement into format that can be deal with function calculate_with_input()
        statement = statement.replace(statement[:3], f"{statement[:3].lower()}(")
        statement = statement.replace(" : ", ", ")
        statement = statement + " )"
    elif is_number(statement):
        p_list = []
    elif statement == "none":
        p_list = [] 
        statement = None
    else:
        p_list = string_to_formula_basic(statement)

    return p_list, statement


def get_params_input(
        p_list: list = None):
    """
    Ask for user input for all elements in the parameter list.

    @param: p_list: list containing strings represent the required parameters. 

    @return: param_val_dict: dictionary in which each (key, val) paire is the string of parameter name and input number (in string format).
    """
    # this is only used for the terminal end use (test), not for GUI
    param_val_dict = {}
    for p in p_list:
        value = input(f"Input {p}: ")
        param_val_dict[p] = value
    
    return param_val_dict


def calculate_with_input(
        statement: str = None, 
        param_val_dict: dict = None):
    """
    Given string description of a formular and dictionary of value for each parameter, do calculation.

    @param: statement: statement: string containing formula.
    @param: param_val_dict: dictionary in which each (key, val) paire is the string of parameter name and input number (in string format).

    @return: return_value: number of the minimum parking requirement calculated by the given formula.
    """
    # use the dictionary of param with input data, calculate the formula statement
    for key in param_val_dict.keys():
        statement = statement.replace(key+" ", param_val_dict[key])

    # calculate and take the ceil
    return_value = math.ceil(eval(statement))

    return return_value



        