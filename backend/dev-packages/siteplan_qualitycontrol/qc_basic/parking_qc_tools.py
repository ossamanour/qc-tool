"""
Functions of tools for parking quality control (local database).
"""
import os
from pathlib import Path
import pandas as pd
from pandas import DataFrame


def get_parking_usage_info(
        parking_requirement_df: DataFrame = None):
    """
    Read in the parking requirement.

    @param: parking_requirement_df: dataframe containing parking requirement, local database.

    @return: usage_type: name for the usages.
    @return: usage_list: list containing all supported usages.
    """
    usage_type = list(parking_requirement_df.keys())[0]
    usage_list = list(parking_requirement_df[usage_type])
    return usage_type, usage_list


def get_parking_requirement_info(
        parking_requirement_df: DataFrame = None, 
        usage: str = None):
    """
    Get the parking requirement for the input usage.

    @param: parking_requirement_df: dataframe containing parking requirement, local database.
    @param: usage: string of the chosen land usage.

    @return: requrement: string of the parking requirement for the input usage.
    @return: statement: string of formula statement for the parking requirement.
    """
    usage_type = list(parking_requirement_df.keys())[0]
    requirement = parking_requirement_df.loc[parking_requirement_df[usage_type] == usage, "Requirement"].values[0]
    statement = parking_requirement_df.loc[parking_requirement_df[usage_type] == usage, "Formula"].values[0]
    return requirement, statement


def analysis_condition_question(
        statement: str = None, 
        level: int = 1):
    """
    Function to analysis the statement with condition.

    @param: statemnt: string of the formula statement.
    @param: level: number indicated the level of condition expression.

    @return: condition_str: string all the condition statement. 
    @return: choice_state: dictionary of the choices for the condition statement.
    """
    # for level 1, the statement is marked using "[question] ? [state1] : [state2]"
    # for level 2, the statement is marked using "[question] ?? [state1] :: [state2]"
    if level == 1:
        mark1 = " ? "
        mark2 = " : "
    else:
        mark1 = " ?? "
        mark2 = " :: "
    
    # condition statement
    loc1 = statement.find(mark1)
    loc2 = statement.find(mark2)
    condition_str = statement[:loc1]
    statement1 = statement[loc1+3:loc2]
    statement2 = statement[loc2+3:]

    # analysis condition string
    # there might be YES/NO question or choice question
    if condition_str.find(" OR ") == -1:
        choice1 = "YES"
        choice2 = "NO"
    else:
        loc_or = condition_str.find(" OR ")
        choice1 = condition_str[:loc_or]
        choice2 = condition_str[loc_or+4:]

    choice_state = {choice1: statement1, 
                    choice2: statement2}

    return condition_str, choice_state


