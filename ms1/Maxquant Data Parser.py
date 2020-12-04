import pandas as pd
import numpy as np
pd.options.display.width = 0
fp = r"C:\Users\ankur\Documents\MS Data\2020-09-17 E coli Thermo & mzXML MQ matching\mzXML MQ E coli WT 1 Rep 1.txt"

def process_maxquant_raw_results(fp):

    mq_df_2 = pd.read_table(fp, low_memory=False)
    mq_df_2.rename(columns={list(mq_df_2)[1]: 'ID'},inplace=True)
    mq_df_2.to_excel('mzXML MQ E coli WT 1 Rep 1.xlsx')

filepath = r"C:\Users\ankur\Documents\Code\MS1 Matching\Mass-Spec-MS1-Analysis\Thermo MQ results E coli WT 1 Rep 1.xlsx"

def maxquant_file_reader(filepath):

    maxquant_df = pd.read_excel(filepath)
    maxquant_df['inferredStructure'] = np.nan
    maxquant_df['theo_mwMonoisotopic'] = np.nan
    maxquant_df.rename(columns={'Retention time': 'rt', 'Mass': 'mwMonoisotopic', 'Intensity': "maxIntensity"},
                               inplace=True)
    focused_maxquant_df = maxquant_df[['ID', 'mwMonoisotopic', 'rt', 'Retention length', 'maxIntensity', 'inferredStructure', 'theo_mwMonoisotopic']]
    cols_order = ['ID', 'rt', 'Retention length', 'mwMonoisotopic', 'theo_mwMonoisotopic', 'inferredStructure', 'maxIntensity', ]
    focused_maxquant_df = focused_maxquant_df[cols_order]


    return focused_maxquant_df


process_maxquant_raw_results(fp)
result_df = maxquant_file_reader(filepath)
print(result_df.head())
result_df.to_excel('mzXML MQ E coli WT 1 Rep 1_formatted.xlsx')