import pandas as pd

def validate_raw_data_df(raw_data_df):
    
    if not isinstance(raw_data_df, pd.DataFrame):
        raise('raw_data_df must be a DataFrame.')

def validate_theo_masses_df(theo_masses_df):

    if not isinstance(theo_masses_df, pd.DataFrame):
        raise('theo_masses_df must be a DataFrame.')

def validate_rt_window(rt_window):

    if not isinstance(rt_window, float):
        raise('rt_window must be a float.')

def validate_enabled_mod_list(enabled_mod_list):

    if not isinstance(enabled_mod_list, list):
        raise('enabled_mod_list must be a list.')

def validate_user_ppm(user_ppm):

    if not isinstance(user_ppm, int):
        raise('user_ppm must be an int.')