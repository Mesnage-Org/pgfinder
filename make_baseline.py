import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation

# Set mass database and modifications
csv_filepath = "data/masses/e_coli_monomer_masses.csv"
theo_masses = pgio.theo_masses_reader(csv_filepath)
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

# Generate maxquant baseline
mq_filepath = "data/maxquant_test_data.txt"
masses_mq = pgio.ms_file_reader(mq_filepath)
validation.validate_raw_data_df(masses_mq)
results = matching.data_analysis(masses_mq, theo_masses, 0.5, mod_test, 10)
pgio.dataframe_to_csv_metadata(save_filepath="./data/", output_dataframe=results, filename="baseline_output_mq.csv")

# Generate ftrs baseline
ftrs_filepath = "data/ftrs_test_data.ftrs"
masses_ftrs = pgio.ms_file_reader(ftrs_filepath)
validation.validate_raw_data_df(masses_ftrs)
results = matching.data_analysis(masses_ftrs, theo_masses, 0.5, mod_test, 10)
pgio.dataframe_to_csv_metadata(save_filepath="./data/", output_dataframe=results, filename="baseline_output_ftrs.csv")
