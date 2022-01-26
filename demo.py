import pgfinder.matching as matching
import pgfinder.validation as validation

mq_filepath = "data/maxquant_test_data.txt"
csv_filepath = "data/masses/e_coli_monomer_masses.csv"

mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']

results = matching.match(mq_filepath, csv_filepath, 0.5, mod_test, 10)

print(results.attrs['metadata'])
print(results)

matching.dataframe_to_csv_metadata(save_filepath='./', output_dataframe=results)
