import numpy as np
import pandas as pd

def validate_raw_data_df(raw_data_df):

    if not isinstance(raw_data_df, pd.DataFrame):
        raise('raw_data_df must be a DataFrame.')

    colnames = ['ID',
                'rt', 
                'rt_length', 
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
                np.dtype('float64'),
                np.dtype('float64'),
                np.dtype('float64'),
                np.dtype('float64')]

    if raw_data_df.dtypes.to_list()!=coltypes:
        raise('raw_data_df column data types are incorrect')

def validate_theo_masses_df(theo_masses_df):

    if not isinstance(theo_masses_df, pd.DataFrame):
        raise('theo_masses_df must be a DataFrame.')

    colnames = ['Structure', 'Monoisotopicmass']

    if theo_masses_df.columns.to_list()!=colnames:
        raise('theo_masses_df column names are incorrect')

    coltypes = [np.dtype('O'), np.dtype('float64')]

    if theo_masses_df.dtypes.to_list()!=coltypes:
        raise('theo_masses_df column data types are incorrect')

def validate_rt_window(rt_window):

    if not isinstance(rt_window, float):
        raise('rt_window must be a float.')
    # todo: range?

def validate_enabled_mod_list(enabled_mod_list):

    if not isinstance(enabled_mod_list, list):
        raise('enabled_mod_list must be a list.')

    allowed_mods = ['Sodium',
                    'Potassium',
                    'Anhydro',
                    'DeAc',
                    'Deacetyl_Anhydro',
                    'Nude',
                    'Decay',
                    'Amidation',
                    'Amidase',
                    'Double_Anh',
                    'Multimers',
                    'multimers_Glyco',
                    'Multimers_Lac']

    if not all(item in allowed_mods for item in enabled_mod_list):
        raise('Requested modification(s) not recognised.')

def validate_user_ppm(user_ppm):

    if not isinstance(user_ppm, int):
        raise('user_ppm must be an int.')
    # todo: range?