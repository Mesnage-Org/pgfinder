import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation

ftrs_filepath = "data/ftrs_test_data.ftrs"
csv_filepath = "data/masses/e_coli_monomer_masses.csv"

masses = pgio.ms_file_reader(ftrs_filepath)
validation.validate_raw_data_df(masses)

theo_masses = pgio.theo_masses_reader(csv_filepath)
validation.validate_theo_masses_df(theo_masses)

mod_test = [
    "Sodium",
    "Potassium",
    "Anh",
    "DeAc",
    "DeAc_Anh",
    "Nude",
    "Decay",
    "Amidation",
    "Amidase",
    "Double_Anh",
    "multimers_Glyco",
]

results = matching.data_analysis(masses, theo_masses, 0.5, mod_test, 10)

print(f"File            : {results.attrs['file']}")
print(f"Masses File     : {results.attrs['file']}")
print(f"rt_window       : {results.attrs['rt_window']}")
print(f"modifications   : {results.attrs['modifications']}")
print(f"ppm             : {results.attrs['ppm']}")
print(results)

pgio.dataframe_to_csv_metadata(save_filepath="./", output_dataframe=results)
