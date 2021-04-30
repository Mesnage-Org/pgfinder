import pgfinder.matching as matching

csv_filepath = "data/masses/e_coli_monomer_masses.csv"
mq_file_name = "data/maxquant_test_data.txt"

raw_data = matching.maxquant_file_reader(mq_file_name)
theo_masses = matching.theo_masses_reader(csv_filepath)
mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']
results = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)

results.to_csv("data/baseline_output.csv")