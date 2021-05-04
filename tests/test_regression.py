import pandas as pd
import pgfinder.matching as matching
import pgfinder.validation as validation

def test_matching_baseline():
    '''Test that output of the major function in the module is unchanged.'''
    masses_file_name = "data/masses/e_coli_monomer_masses.csv"
    mq_file_name = "data/maxquant_test_data.txt"

    raw_data = matching.maxquant_file_reader(mq_file_name)
    validation.validate_raw_data_df(raw_data)

    theo_masses = matching.theo_masses_reader(masses_file_name)
    validation.validate_theo_masses_df(theo_masses)

    mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']
    validation.validate_enabled_mod_list(mod_test)

    output_df = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)
    
    baseline_df = pd.read_csv("data/baseline_output.csv", index_col=0)

    pd.testing.assert_frame_equal(output_df, baseline_df)