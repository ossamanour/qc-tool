"""
Functions related to Pandas DataFrame.
"""
import pandas as pd
from pandas import DataFrame
import numpy as np
from ast import literal_eval


def dataframe_save(
        df: DataFrame = None, 
        save_path: str = None):
    """
    Read in data frame and save. Special deal with cells containing numpy array.

    @param: df: dataframe to be saved.
    @param: save_path: path to save the dataframe.
    """
    df_save = df.copy()
    for key in df.keys():
        if isinstance(df_save.iloc[0][key], np.ndarray):
            df_save[key] = df_save[key].apply(lambda x: np.array(x).tolist())
    df_save.to_csv(save_path, index=False)


def arrow_angle_read_csv(
        filepath: str = None):
    """
    Read in dataframe which stores the arrow angle information. Special process to read in contour, tip_pt, and mid_pt.

    @param: filepath: string for the dataframe file path.
    
    @return: arrow_angle_df: dataframe containing arrow angle information.
    """
    arrow_angle_df = pd.read_csv(filepath, 
                                 converters={'contour': literal_eval,
                                             'tip_pt': literal_eval, 
                                             'mid_pt': literal_eval})
    return arrow_angle_df


def keynote_read_csv(
        filepath: str = None):
    """
    Read in dataframe which stores the keynote inforamtion. Special process to read in contour, and hierarchy.

    @param: filepath: string for the dataframe file path.

    @return: keynote_df: dataframe containing keynote information. 
    """
    keynote_df = pd.read_csv(filepath, 
                             converters={'contour': literal_eval, 
                                         'hierarchy': literal_eval})
    return keynote_df