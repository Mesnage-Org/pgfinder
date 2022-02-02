import pandas as pd
import pytest
import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation

@pytest.fixture
def masses_file_name():
    return "data/masses/e_coli_monomer_masses.csv"

@pytest.fixture
def mod_test():
    """Modifications used in regression testing."""
    return ['Sodium','Potassium','Anhydro','DeAc','Deacetyl_Anhydro','Nude','Decay','Amidation','Amidase','Double_Anh','multimers_Glyco']

@pytest.fixture
def mq_file_name():
    return "data/maxquant_test_data.txt"

@pytest.fixture
def mq_baseline_df():
    return pd.read_csv("data/baseline_output_mq.csv", index_col=0)

@pytest.fixture
def ftrs_file_name():
    return "data/ftrs_test_data.ftrs"

@pytest.fixture
def ftrs_baseline_df():
    return pd.read_csv("data/baseline_output_ftrs.csv", index_col=0)

def test_matching_mq_baseline(masses_file_name, mq_file_name, mod_test, mq_baseline_df):
    '''Test that output of the major function in the module is unchanged.'''
    
    raw_data = pgio.maxquant_file_reader(mq_file_name)
    validation.validate_raw_data_df(raw_data)

    theo_masses = pgio.theo_masses_reader(masses_file_name)
    validation.validate_theo_masses_df(theo_masses)
    
    validation.validate_enabled_mod_list(mod_test)

    output_df = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)
    
    pd.testing.assert_frame_equal(output_df, mq_baseline_df)

def test_matching_ftrs_baseline(masses_file_name, ftrs_file_name, mod_test, ftrs_baseline_df):
    """Test that output of the major function in the module is unchanged."""
    
    raw_data = matching.ftrs_reader(ftrs_file_name)
    validation.validate_raw_data_df(raw_data)

    theo_masses = matching.theo_masses_reader(masses_file_name)
    validation.validate_theo_masses_df(theo_masses)
    
    validation.validate_enabled_mod_list(mod_test)

    output_df = matching.data_analysis(raw_data, theo_masses, 0.5, mod_test, 10)
    
    pd.testing.assert_frame_equal(output_df, ftrs_baseline_df)