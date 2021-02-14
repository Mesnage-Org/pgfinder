import numpy as np
import pandas as pd

def validate_raw_data_df(raw_data_df):

    if not isinstance(raw_data_df, pd.DataFrame):
        raise('raw_data_df must be a DataFrame.')

    colnames = ['ID', 
                'xicStart', 
                'xicEnd', 
                'feature', 
                'corrMax', 
                'ionCount', 
                'chargeOrder', 
                'maxIsotopeCount', 
                'rt', 
                'mwMonoisotopic', 
                'theo_mwMonoisotopic', 
                'inferredStructure', 
                'maxIntensity']

    if raw_data_df.columns.to_list()!=colnames:
        raise('raw_data_df column names are incorrect')

    #todo: maybe these can be relaxed - or maybe ranges needed?
    coltypes = [np.dtype('int64'), 
                np.dtype('float64'), 
                np.dtype('float64'), 
                np.dtype('int64'), 
                np.dtype('float64'), 
                np.dtype('int64'), 
                np.dtype('O'), 
                np.dtype('int64'), 
                np.dtype('float64'), 
                np.dtype('float64'), 
                np.dtype('float64'), 
                np.dtype('float64'), 
                np.dtype('int64')]

    if raw_data_df.dtypes.to_list()!=coltypes:
        raise('raw_data_df column data types are incorrect')

def validate_theo_masses_df(theo_masses_df):

    if not isinstance(theo_masses_df, pd.DataFrame):
        raise('theo_masses_df must be a DataFrame.')
    # todo: check column names and types

def validate_rt_window(rt_window):

    if not isinstance(rt_window, float):
        raise('rt_window must be a float.')
    # todo: range?

def validate_enabled_mod_list(enabled_mod_list):

    if not isinstance(enabled_mod_list, list):
        raise('enabled_mod_list must be a list.')
    # todo: check against allowable mod names

def validate_user_ppm(user_ppm):

    if not isinstance(user_ppm, int):
        raise('user_ppm must be an int.')
    # todo: range?