import pandas as pd
import pytest
import pgfinder.matching as matching
import pgfinder.validation as validation

@pytest.fixture
def raw_data_filename():
    return "data/maxquant_test_data.txt"

@pytest.fixture
def raw_data_no_match_filename():
    return "data/maxquant_test_data_no_match.txt"

@pytest.fixture
def theo_masses_filename():
    return "data/masses/e_coli_monomer_masses.csv"

@pytest.fixture
def raw_data(raw_data_filename):
    my_raw_data = matching.maxquant_file_reader(raw_data_filename)
    validation.validate_raw_data_df(my_raw_data) 
    return my_raw_data

@pytest.fixture
def raw_data_no_match(raw_data_no_match_filename):
    my_raw_data_no_match = matching.maxquant_file_reader(raw_data_no_match_filename)
    validation.validate_raw_data_df(my_raw_data_no_match) 
    return my_raw_data_no_match

@pytest.fixture
def theo_masses(theo_masses_filename):
    my_theo_masses = matching.theo_masses_reader(theo_masses_filename)
    validation.validate_theo_masses_df(my_theo_masses)
    return my_theo_masses

@pytest.fixture
def ppm():
    return 10

def test_filtered_theo(raw_data, theo_masses, ppm):
    # this crude test just shows that the code runs
    # a better test would check that the data frame returned is correct
    obs_monomers_df = matching.filtered_theo(raw_data, theo_masses, ppm)

def test_filtered_theo_no_match(raw_data_no_match, theo_masses, ppm):
    obs_monomers_df = matching.filtered_theo(raw_data_no_match, theo_masses, ppm)