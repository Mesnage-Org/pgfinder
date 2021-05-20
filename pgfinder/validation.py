import io
import pkgutil
import numpy as np
import pandas as pd

def allowed_modifications():
    '''
    Returns allowable modifications stored in a `.csv` config file. `.csv` is chosen for consistency of data storage over the project.    
    :return list:
    '''
    data = pkgutil.get_data(__name__, "config/allowed_modifications.csv")    
    allowed_modifications_df  = pd.read_csv(io.BytesIO(data), header=None)
    return allowed_modifications_df[0].tolist()

def validate_raw_data_df(raw_data_df):

    if not isinstance(raw_data_df, pd.DataFrame):
        raise ValueError('raw_data_df must be a DataFrame.')
    
    if isinstance(raw_data_df, pd.DataFrame):
        print("File is okay")


    colnames = ['ID',
                'rt',
                'mwMonoisotopic',
                'theo_mwMonoisotopic',
                'inferredStructure',
                'maxIntensity']


    if not set(colnames).issubset(set(raw_data_df.columns.to_list())):
        raise('raw_data_df column names are incorrect')

def validate_theo_masses_df(theo_masses_df):

    if not isinstance(theo_masses_df, pd.DataFrame):
        raise ValueError('theo_masses_df must be a DataFrame.')

    colnames = ['Structure', 'Monoisotopicmass']

    if theo_masses_df.columns.to_list()!=colnames:
        raise ValueError('theo_masses_df column names are incorrect')

    coltypes = [np.dtype('O'), np.dtype('float64')]

    if theo_masses_df.dtypes.to_list()!=coltypes:
        raise ValueError('theo_masses_df column data types are incorrect')

def validate_rt_window(rt_window):

    if not isinstance(rt_window, float):
        raise ValueError('rt_window must be a float.')
    # todo: range?

def validate_enabled_mod_list(enabled_mod_list):

    if not isinstance(enabled_mod_list, list):
        raise ValueError('enabled_mod_list must be a list.')

    allowed_mods = allowed_modifications()

    if not all(item in allowed_mods for item in enabled_mod_list):
        raise ValueError('Requested modification(s) not recognised.')

def validate_user_ppm(user_ppm):

    if not isinstance(user_ppm, int):
        raise ValueError('user_ppm must be an int.')
    # todo: range?