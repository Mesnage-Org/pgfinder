import pgfinder.matching as matching

# Set mass database and modifications
csv_filepath = "data/masses/e_coli_monomer_masses.csv"
theo_masses = matching.theo_masses_reader(csv_filepath)
mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']

# Generate maxquant baseline
mq_file_name = "data/maxquant_test_data.txt"
raw_data_mq = matching.maxquant_file_reader(mq_file_name)
results = matching.data_analysis(raw_data_mq, theo_masses, 0.5, mod_test, 10)
results.to_csv("data/baseline_output_mq.csv")

# Generate ftrs baseline
ftrs_file_name = "data/ftrs_test_data.ftrs"
raw_data_ftrs = matching.ftrs_reader(ftrs_file_name)
results = matching.data_analysis(raw_data_ftrs, theo_masses, 0.5, mod_test, 10)
results.to_csv("data/baseline_output_ftrs.csv")
