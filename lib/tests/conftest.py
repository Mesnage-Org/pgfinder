"""Fixtures for various tests."""

import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import pgfinder.pgio as pgio
import pgfinder.validation as validation

BASE_DIR = Path.cwd()
RESOURCES_DIR = BASE_DIR / "tests" / "resources"
DATA_DIR = RESOURCES_DIR / "data"


# test_matching.py fixtures
@pytest.fixture
def raw_data_filename():
    return str(DATA_DIR / "maxquant_test_data.txt")


@pytest.fixture
def raw_data_no_match_filename():
    return str(DATA_DIR / "maxquant_test_data_no_match.txt")


@pytest.fixture
def theo_masses_filename():
    return str(DATA_DIR / "masses" / "e_coli_monomer_masses.csv")


@pytest.fixture
def raw_data(raw_data_filename):
    my_raw_data = pgio.ms_file_reader(raw_data_filename)
    validation.validate_raw_data_df(my_raw_data)
    return my_raw_data


@pytest.fixture
def raw_data_no_match(raw_data_no_match_filename):
    my_raw_data_no_match = pgio.ms_file_reader(raw_data_no_match_filename)
    validation.validate_raw_data_df(my_raw_data_no_match)
    return my_raw_data_no_match


@pytest.fixture
def theo_masses(theo_masses_filename):
    my_theo_masses = pgio.theo_masses_reader(theo_masses_filename)
    validation.validate_theo_masses_df(my_theo_masses)
    return my_theo_masses


@pytest.fixture
def ipywidgets_upload_output(ftrs_file_name):
    return {
        "name": "ftrs_test_data.ftrs",
        "type": "",
        "size": 14274560,
        "content": open(ftrs_file_name, "rb").read(),
        "last_modified": datetime.datetime(2022, 2, 2, 11, 6, 9, 951000, tzinfo=datetime.timezone.utc),
    }


@pytest.fixture
def ipywidgets_upload_output_theo(theo_masses_file_name):
    return {
        "name": "e_coli_monomer_masses.csv",
        "type": "text/csv",
        "size": 4975,
        "content": open(theo_masses_file_name, "rb").read(),
        "last_modified": datetime.datetime(2022, 3, 13, 19, 47, 12, 102000, tzinfo=datetime.timezone.utc),
    }


@pytest.fixture
def ppm():
    return 10


@pytest.fixture
def obs_theoretical_molecular_weights() -> pd.DataFrame:
    """Provides a simple list of theoretical and observed molecular weights for testing calculate_delta_ppm()."""
    return pd.DataFrame({"mwMonoisotopic": [10, 20, 300], "theo_mwMonoisotopic": [9, "15, 21", "298, 300, 301"]})


# test_regression.py fixtures
@pytest.fixture
def theo_masses_file_name():
    return str(DATA_DIR / "masses" / "e_coli_monomer_masses.csv")


@pytest.fixture
def theo_masses_df(theo_masses_file_name):
    return pgio.theo_masses_reader(theo_masses_file_name)


@pytest.fixture
def mod_test():
    """Modifications used in regression testing."""
    return validation.allowed_modifications()


@pytest.fixture
def mq_file_name():
    return str(DATA_DIR / "maxquant_test_data.txt")


@pytest.fixture
def mq_test_df(mq_file_name):
    return pgio.ms_file_reader(mq_file_name)


@pytest.fixture(params=["ftrs_test_data_5.2.ftrs", "ftrs_test_data_3.11.ftrs"])
def ftrs_file_name(request):
    return str(DATA_DIR / request.param)


@pytest.fixture
def ftrs_test_df(ftrs_file_name):
    return pgio.ms_file_reader(ftrs_file_name)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Return a dummy data frame for tests."""
    return pd.DataFrame(
        {
            "id": [1, 1, 2, 2, 3, 4, 4],
            "obs": [1, 5645.35435454, 879546.3924093, 789.3, 6541321.2, 10, 10],
            "exp": [2, 3954.49849514, 879546.8974916, 780.4, 6541329.7, 11, 11],
            "inferred": ["A", "B", "C", "D", "E", "F", "G"],
            "intensity": [2, 2, 3, 3, 5, 6, 6],
        }
    ).convert_dtypes()


@pytest.fixture
def df_diff_ppm(sample_df: pd.DataFrame) -> pd.DataFrame:
    """Return a target data frame for tests with diff_pm included."""
    DELTA_DF = pd.DataFrame(
        {
            "Delta (ppm)": [
                -500000.0,
                427577.82345296827,
                -0.5742528357381609,
                11404.407996,
                -1.299430,
                -90909.09090909091,
                -90909.09090909091,
            ]
        }
    )
    DELTA_DF = pd.concat([sample_df, DELTA_DF], axis=1)
    DELTA_DF = DELTA_DF.convert_dtypes()
    return DELTA_DF[["id", "obs", "exp", "Delta (ppm)", "inferred", "intensity"]]


@pytest.fixture
def df_likely_structure() -> pd.DataFrame:
    """Return a data frame with the lowest ppm differences and their intensity derived."""
    return pd.DataFrame(
        {
            "id": [1, 1, 2, 2, 3, 4, 4],
            "obs": [5645.354355, 1.0, 879546.392409, 789.3, 6541321.2, 10.0, 10.0],
            "exp": [3954.498495, 2.0, 879546.897492, 780.4, 6541329.7, 11.0, 11.0],
            "diff_ppm": [427577.823453, -500000.0, -0.574253, 11404.407996, -1.29943, -90909.090909, -90909.090909],
            "inferred": ["B", "A", "C", "D", "E", "F", "G"],
            "intensity": [2, 1, 3, 4, 5, 6, 6],
            "lowest ppm": [427577.823453, np.nan, -0.574253, np.nan, -1.29943, -90909.090909, -90909.090909],
            "Inferred Max Intensity": [2.0, np.nan, 3.0, np.nan, 5.0, 6.0, 6.0],
        }
    )


@pytest.fixture
def consolidated() -> pd.DataFrame:
    """Return an expected consoldiated dataframe to test against."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "lowest ppm": ["B", "C", "E", "F,   G"],
            "Inferred Max Intensity": [2.0, 3.0, 5.0, 6.0],
        }
    )


@pytest.fixture
def unconsolidated_df() -> pd.DataFrame:
    """Return a combined unconsolidated and consolidated dataframe to test against."""
    return pd.read_csv(RESOURCES_DIR / "unconsolidated.csv")


@pytest.fixture
def unconsolidated_and_consolidated_df() -> pd.DataFrame:
    """Return a combined unconsolidated and consolidated dataframe to test against."""
    return pd.read_csv(RESOURCES_DIR / "consolidated.csv")
