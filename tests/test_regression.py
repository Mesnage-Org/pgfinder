import pandas as pd
import ms1.matching as matching

def test_matching_baseline():
    '''Test that output of the major function in the module is unchanged.'''
    masses_file_name = "data/test_masses.csv"
    ftrs_file_name = "data/test_ms_data.ftrs"

    raw_data = matching.ftrs_reader(ftrs_file_name)
    theo_masses = matching.theo_masses_reader(masses_file_name)
    mod_test = ['Sodium','Nude', 'DeAc']

    output_df = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)
    
    baseline_df = pd.read_csv("data/baseline_output.csv", index_col=0)

    pd.testing.assert_frame_equal(output_df, baseline_df)