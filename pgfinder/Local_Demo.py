import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation
from pgfinder import MULTIMERS, MOD_TYPE, MASS_TO_CLEAN
import pandas as pd
from decimal import *

ftrs_filepath = "data/ftrs_test_data.ftrs"
consol_test_data_filepath = "data/long_format_test_data.txt"
csv_filepath = "data/masses/e_coli_monomer_masses.csv"

masses = pgio.ms_file_reader(consol_test_data_filepath)
validation.validate_raw_data_df(masses)

theo_masses = pgio.theo_masses_reader(csv_filepath)
validation.validate_theo_masses_df(theo_masses)

mod_test = ['Decay']

results = matching.data_analysis(masses,theo_masses,0.5,mod_test,10,True)

print (results)


    

    

#pgio.dataframe_to_csv_metadata(save_filepath='./', output_dataframe=results)
