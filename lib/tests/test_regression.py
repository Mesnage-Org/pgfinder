"""Regression test"""

import pandas as pd

import pgfinder.matching as matching
import pgfinder.pgio as pgio
import pgfinder.validation as validation


def test_matching_mq_baseline(
    regtest, mq_test_df: pd.DataFrame, theo_masses_df: pd.DataFrame, mod_test, tmp_path
) -> None:
    """Test that output of the major function in the module is unchanged."""

    validation.validate_raw_data_df(mq_test_df)
    validation.validate_theo_masses_df(theo_masses_df)

    results = matching.data_analysis(mq_test_df, theo_masses_df, 0.5, mod_test, 10, 1)

    output_filepath = pgio.dataframe_to_csv_metadata(
        save_filepath=tmp_path, output_dataframe=results, filename="output_mq.csv"
    )
    output_df = pd.read_csv(output_filepath, index_col=None)
    # Because versions change based on commits due to setuptools_scm we fix the version so tests are consistent
    output_df.iloc[6, 0] = "version : pgfinder"

    print(output_df.to_csv(index=False), file=regtest)


def test_matching_ftrs_baseline(
    regtest, ftrs_test_df: pd.DataFrame, theo_masses_df: pd.DataFrame, mod_test, tmp_path
) -> None:
    """Test that output of the major function in the module is unchanged."""

    validation.validate_raw_data_df(ftrs_test_df)
    validation.validate_theo_masses_df(theo_masses_df)

    results = matching.data_analysis(ftrs_test_df, theo_masses_df, 0.5, mod_test, 10, 1)

    output_filepath = pgio.dataframe_to_csv_metadata(
        save_filepath=tmp_path, output_dataframe=results, filename="output_ftrs.csv"
    )

    output_df = pd.read_csv(output_filepath, index_col=None)
    # Because versions change based on commits due to setuptools_scm we fix the version so tests are consistent
    output_df.iloc[6, 0] = "version : pgfinder"

    print(output_df.to_csv(index=False), file=regtest)
