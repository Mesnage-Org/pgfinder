import pandas as pd
import ms1.matching as matching

def test_matching_baseline():
    '''Test that output of the major function in the module is unchanged.'''
    masses_file_name = "data/E_coli_disaccharides_monomers_only.csv"
    ftrs_file_name = "data/OT_200124_Ecoli_WT_1_Rep1.ftrs"

    raw_data = matching.ftrs_reader(ftrs_file_name)
    theo_masses = matching.theo_masses_reader(masses_file_name)
    mod_test = ['Sodium','Nude', 'DeAc']

    results = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test)
    
    baseline_df = pd.read_csv("data/baseline_output.csv")
    output_df = pd.read_csv("output.csv")

    pd.testing.assert_frame_equal(output_df, baseline_df)