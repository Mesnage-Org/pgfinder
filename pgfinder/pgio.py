from typing import Union
import pathlib
from pathlib import Path
import datetime
import os
import pandas as pd
import sqlite3
import numpy as np
import yaml

def ftrs_reader(filePath: str):
    '''Reads FTRS file from Byos
    :param filePath:
    :return dataframe:
    '''

    with sqlite3.connect(filePath) as db:

        sql = "SELECT * FROM Features"
        #Reads sql database into dataframe
        ff = pd.read_sql(sql, db)
        # adds inferredStructure column
        ff['inferredStructure'] = np.nan
        # adds theo_mwMonoisotopic column
        ff['theo_mwMonoisotopic'] = np.nan
        # Renames columns to expected column heading required for data_analysis function
        ff.rename(columns={'Id': 'ID', 'apexRetentionTimeMinutes': 'rt', 'apexMwMonoisotopic': 'mwMonoisotopic', 'maxAveragineCorrelation': 'corrMax' }, inplace=True)
        # Desired column order
        cols_order = ['ID', 'xicStart', 'xicEnd', 'feature', 'corrMax', 'ionCount', 'chargeOrder', 'maxIsotopeCount',
                      'rt', 'mwMonoisotopic','theo_mwMonoisotopic', 'inferredStructure', 'maxIntensity', ]
        # Reorder columns in dataframe to desired order.
        ff = ff[cols_order]

        return ff

def theo_masses_reader(filepath: str):

    '''
    Reads theoretical masses files (csv)
    :param filepath:
    :return dataframe:
    '''
    # reads csv files and converts to dataframe
    theo_masses_df = pd.read_csv(filepath)

    return theo_masses_df

def maxquant_file_reader(filepath: str):
    '''
        Reads maxquant files and outputs data as a dataframe

    :param filepath (file should be a text file):
    :return dataframe:
    '''

    # reads file into dataframe
    maxquant_df = pd.read_table(filepath, low_memory=False)
    # adds inferredStructure column
    maxquant_df['inferredStructure'] = np.nan
    # adds theo_mwMonoisotopic column
    maxquant_df['theo_mwMonoisotopic'] = np.nan
    # insert dataframe index as a column
    maxquant_df.reset_index(level=0, inplace=True)
    # Renames columns to expected column heading required for data_analysis function
    maxquant_df.rename(columns={'index': 'ID','Retention time': 'rt', 'Retention length': 'rt_length',
                                'Mass': 'mwMonoisotopic', 'Intensity': "maxIntensity"},
                               inplace=True)
    # Keeps only essential columns, all extraneous columns are left out.
    focused_maxquant_df = maxquant_df[['ID', 'mwMonoisotopic', 'rt', 'rt_length', 'maxIntensity', 'inferredStructure',
                                       'theo_mwMonoisotopic']]
    # Desired column order
    cols_order = ['ID', 'rt', 'rt_length', 'mwMonoisotopic', 'theo_mwMonoisotopic', 'inferredStructure', 'maxIntensity']
    # Reorder columns in dataframe to desired order.
    focused_maxquant_df = focused_maxquant_df[cols_order]


    return focused_maxquant_df

def dataframe_to_csv(save_filepath: str, filename:str, output_dataframe: pd.DataFrame):
    '''
    Writes dataframe to csv file at desired file location
    :param save_filepath:
    :param filename:
    :param output_dataframe:
    :return csv file:
    '''

    #Combine save location and desired file name with correct formatting for output as csv file.
    write_location = save_filepath + '/' + filename + '.csv'
    output_dataframe.to_csv(write_location, index=False)

def dataframe_to_csv_metadata(save_filepath: Union[str, Path], output_dataframe: pd.DataFrame, filename: Union[str, Path] = None) -> Union[str, Path]:

    filename = pathlib.Path(filename or default_filename())

    write_location = os.path.join(save_filepath, filename)

    metadata_string = yaml.dump(output_dataframe.attrs['metadata'])

    output_dataframe.insert(0, metadata_string.replace("\n", " "), "")

    output_dataframe.to_csv(write_location, index=False)

    return write_location

def default_filename():
    now = datetime.datetime.now()
    date_time = now.strftime('%Y-%m-%d_%H-%M-%S')
    filename = 'results_' + date_time + '.csv'
    
    return filename
