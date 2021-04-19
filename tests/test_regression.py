import pandas as pd
import ms1.matching as matching
import ms1.validation as validation

def test_matching_baseline():
    '''Test that output of the major function in the module is unchanged.'''
    masses_file_name = "data/test_masses.csv"
    ftrs_file_name = "data/test_ms_data.ftrs"

    raw_data = matching.ftrs_reader(ftrs_file_name)
    validation.validate_raw_data_df(raw_data)

    theo_masses = matching.theo_masses_reader(masses_file_name)
    validation.validate_theo_masses_df(theo_masses)

    mod_test = ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']
    validation.validate_enabled_mod_list(mod_test)

    output_df = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)
    
    baseline_df = pd.read_csv("data/baseline_output.csv", index_col=0)

    pd.testing.assert_frame_equal(output_df, baseline_df)