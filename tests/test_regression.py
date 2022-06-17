import pandas as pd
import pytest
import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation


@pytest.fixture
def theo_masses_file_name():
    return "data/masses/e_coli_monomer_masses.csv"


@pytest.fixture
def theo_masses_df(theo_masses_file_name):
    return pgio.theo_masses_reader(theo_masses_file_name)


@pytest.fixture
def mod_test():
    """Modifications used in regression testing."""
    return [
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


@pytest.fixture
def mq_file_name():
    return "data/maxquant_test_data.txt"


@pytest.fixture
def mq_test_df(mq_file_name):
    return pgio.ms_file_reader(mq_file_name)


@pytest.fixture
def mq_baseline_df():
    return pd.read_csv("data/baseline_output_mq.csv", index_col=0)


@pytest.fixture
def ftrs_file_name():
    return "data/ftrs_test_data.ftrs"


@pytest.fixture
def ftrs_test_df(ftrs_file_name):
    return pgio.ms_file_reader(ftrs_file_name)


@pytest.fixture
def ftrs_baseline_df():
    return pd.read_csv("data/baseline_output_ftrs.csv", index_col=0)


def test_matching_mq_baseline(mq_test_df, theo_masses_df, mod_test, mq_baseline_df, tmp_path):
    """Test that output of the major function in the module is unchanged."""

    validation.validate_raw_data_df(mq_test_df)
    validation.validate_theo_masses_df(theo_masses_df)

    results = matching.data_analysis(mq_test_df, theo_masses_df, 0.5, mod_test, 10)

    output_filepath = pgio.dataframe_to_csv_metadata(
        save_filepath=tmp_path, output_dataframe=results, filename="output_mq.csv"
    )
    output_df = pd.read_csv(output_filepath, index_col=0)

    pd.testing.assert_frame_equal(output_df, mq_baseline_df)


def test_matching_ftrs_baseline(ftrs_test_df, theo_masses_df, mod_test, ftrs_baseline_df, tmp_path):
    """Test that output of the major function in the module is unchanged."""

    validation.validate_raw_data_df(ftrs_test_df)
    validation.validate_theo_masses_df(theo_masses_df)

    results = matching.data_analysis(ftrs_test_df, theo_masses_df, 0.5, mod_test, 10)

    output_filepath = pgio.dataframe_to_csv_metadata(
        save_filepath=tmp_path, output_dataframe=results, filename="output_ftrs.csv"
    )

    output_df = pd.read_csv(output_filepath, index_col=0)

    pd.testing.assert_frame_equal(output_df, ftrs_baseline_df)
