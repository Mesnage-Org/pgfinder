import pgfinder.matching as matching
import pgfinder.validation as validation

csv_filepath = "data/test_masses.csv"
ftrs_filepath = "data/test_ms_data.ftrs"

raw_data = matching.ftrs_reader(ftrs_filepath)
validation.validate_raw_data_df(raw_data)

theo_masses = matching.theo_masses_reader(csv_filepath)
validation.validate_theo_masses_df(theo_masses)

mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','Multimers']
validation.validate_enabled_mod_list(mod_test)

results = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)

print(results)