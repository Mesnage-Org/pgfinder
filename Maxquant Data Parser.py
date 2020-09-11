import pandas as pd
import numpy as np
pd.options.display.width = 0
# filepath = r"G:\Shared drives\MS1 Paper shared drive\Maxquant results\combined\txt\allPeptides.txt"
# # mq_df = pd.read_csv(filepath,sep='  ', engine='python')
# mq_df_2 = pd.read_table(filepath, low_memory=False)
#
# # print(mq_df_2.tail())
#
# raw_data_set_1_df = mq_df_2.loc[mq_df_2['Raw file'] == 'Anderson et al JBC 2019 Planktonic B3.001']
# print(raw_data_set_1_df)
# print(raw_data_set_1_df.shape)
# raw_data_set_1_df.to_excel('Planktonic B3 T1.xlsx')

filepath = r"C:\Users\ankur\Documents\Code\MS1 Matching\Mass-Spec-MS1-Analysis\Planktonic B3 T1.xlsx"

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


result_df = maxquant_file_reader(filepath)
print(result_df.head())