import pgfinder.matching as matching
import pgfinder.pgio as pgio

# Set mass database and modifications
csv_filepath = "data/masses/e_coli_monomer_masses.csv"
theo_masses = pgio.theo_masses_reader(csv_filepath)
mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']

# Generate maxquant baseline
mq_filepath = "data/maxquant_test_data.txt"
results = matching.match(mq_filepath, csv_filepath, 0.5, mod_test, 10)
pgio.dataframe_to_csv_metadata(save_filepath='./data/', output_dataframe=results, filename='baseline_output_mq.csv')


# Generate ftrs baseline
ftrs_filepath = "data/ftrs_test_data.ftrs"
results = matching.match(ftrs_filepath, csv_filepath, 0.5, mod_test, 10)
pgio.dataframe_to_csv_metadata(save_filepath='./data/', output_dataframe=results, filename='baseline_output_ftrs.csv')
