import ms1.matching as matching

csv_filepath = "data/test_masses.csv"
ftrs_filepath = "data/test_ms_data.ftrs"

raw_data = matching.ftrs_reader(ftrs_filepath)
theo_masses = matching.theo_masses_reader(csv_filepath)
mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']
results = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)

results.to_csv("data/baseline_output.csv")