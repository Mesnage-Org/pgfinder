import pandas as pd
import ms1.matching as matching

def test_matching_baseline():
    '''Test that output of the major function in the module is unchanged.'''
    masses_file_name = "data/E_coli_disaccharides_monomers_only.csv"
    ftrs_file_name = "data/OT_200124_Ecoli_WT_1_Rep1.ftrs"
    matching.main(ftrs_file_name, masses_file_name)
    
    baseline_df = pd.read_csv("data/baseline_output.csv")
    output_df = pd.read_csv("output.csv")

    pd.testing.assert_frame_equal(output_df, baseline_df)